from datetime import timedelta
from re import L
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.conf import settings
from django.db.models import Q
import mimetypes

from classes import *
from supportedschools import schools

from .models import Post
from .forms import PostForm, questionPasswordForm

def index(request, school):
    school = school.lower()

    sort = request.GET.get('sort')
    subject = request.GET.get('subject')
    context = {}
    
    if subject:
        posts = Post.objects.filter(school = school, subject=subject)
        context['subject'] = subject
    else:
        posts = Post.objects.filter(school = school)

    if sort == "unsolved":
        posts = posts.filter(solved=False).order_by('-id') 
        context['sort'] = 'unsolved'
    else:
        posts = posts.order_by('-id')

    page = int(request.GET.get('page')) if request.GET.get('page') else 0

    if not posts:
        return render(request, "index.html", {"message":"No questions posted", "subjects": classes})

    next_page_index = (page+1)*settings.LIST_PAGE_SIZE

    if len(posts) <= next_page_index:
        lq = posts[page*settings.LIST_PAGE_SIZE:]
        if not lq:
            raise Http404('Page not found :(')
        context['nextpage'] = None

    else:
        lq = posts[page*settings.LIST_PAGE_SIZE:next_page_index]
        context['nextpage'] = page+1

    if page > 0:
        context['previouspage'] = page-1
    else:
        context['previouspage'] = None

    ip = get_client_ip(request)
    
    context['lq'] = lq
    context["subjects"] = classes
    return render(request, "index.html", context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return request.META.get("HTTP_X_REAL_IP")

def create(request):
    if request.method == "GET":
        return render(request, "create.html", {"subjects": classes, "schools": schools})
    
    elif request.method == "POST":
        
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            last_posts = Post.objects.filter(creation_date__gt=timezone.now()-timedelta(minutes=30))
            qset = Q()
            
            if form.cleaned_data.get('instagram'):
                qset |= Q(instagram=form.cleaned_data.get('instagram'))

            if form.cleaned_data.get('email'):
                qset |= Q(instagram=form.cleaned_data.get('email'))

            if form.cleaned_data.get('phone'):
                qset |= Q(instagram=form.cleaned_data.get('phone'))

            last_posts = last_posts.filter(qset)

            if len(last_posts) >= 5:
                return render(request, "create.html", {"subjects": classes, "schools": schools, "message":"Only 5 questions every 30 mins", })

            new_post = form.save(commit=False)

            if request.session.get('passwords'):
                 request.session['passwords'] = request.session['passwords'].append(new_post.password)
            else:
                request.session['passwords'] = [new_post.password]

            new_post.attachment = request.FILES.get('attachment')

            new_post.save()
           
            return redirect('school', new_post.school)
        print(form.errors)
        return render(request, "create.html", {"subjects": classes, "schools": schools, 'form': form})

def download_file(request, filename):
    fl_path = settings.MEDIA_ROOT / filename
    try:
        fl = open(fl_path, 'rb')
    except:
        raise Http404("File not found :( either you're trying to be cheeky or the file got currupted")
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response

def jqeury_course(request, subject):
    if request.is_ajax and request.method == "GET":
        return JsonResponse({"subject":courses[subject]}, status=200)

def home(request):
    return redirect('school', 'uiuc')
    #return render(request, "home.html", {"schools":schools})

@xframe_options_sameorigin
def question(request, id):
    question = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = questionPasswordForm(request.POST)

        if form.is_valid():
            password = question.password
            if password != form.cleaned_data.get('password'):
                form.add_error('password', 'Wrong password mate :(')
                return render(request, "question.html", {"question": question, "form": form})

            if request.session.get('passwords'):
                 request.session['passwords'] = request.session['passwords'].append(password)
            else:
                request.session['passwords'] = [password]

    return render(request, "question.html", {"question": question})

def solved(request, id):
    if request.is_ajax and request.method == "POST":
        question = get_object_or_404(Post, id=id)
        solved = not question.solved

        question.solved=solved
        question.save()

        return JsonResponse({"solved": solved}, status=200)
