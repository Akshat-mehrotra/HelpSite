from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from sqlalchemy import true
from classes import *
from supportedschools import schools

from .models import Post, PostForm

def index(request, school):
    school = school.lower()
    lq = Post.objects.filter(school = school).order_by('-id')[:50]

    ip = get_client_ip(request)

    if lq: 
        return render(request, "index.html", {"lq":lq, "ip":ip})

    return render(request, "index.html", {"message":"No questions posted"})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create(request):
    if request.method == "GET":
        return render(request, "create.html", {"subjects": classes, "schools": schools})
    
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            ip = get_client_ip(request)

            last_posts = Post.objects.filter(ip=ip, creation_date__gt=timezone.now()-timedelta(minutes=30))
            if len(last_posts) >= 5:
                return render(request, "create.html", {"subjects": classes, "schools": schools, "message":"Only 5 questions every 30 mins", })

            form.cleaned_data['ip'] = ip
            new_post = Post(**form.cleaned_data)
            print(form['price'])
            new_post.save()

            return redirect('school', new_post.school)
        return render(request, "create.html", {"subjects": classes, "schools": schools, 'form': form})

def jqeury_course(request, subject):
    if request.is_ajax and request.method == "GET":
        return JsonResponse({"subject":courses[subject]}, status=200)

def home(request):
    return redirect('school', 'uiuc')
    #return render(request, "home.html", {"schools":schools})

def question(request, id):
    pass

def solved(request, id):
    if request.is_ajax and request.method == "POST":
        checked = True if request.POST['checked'] == 'true' else False
        Post.objects.filter(id=id).update(solved=checked)

        return JsonResponse({"checked": checked}, status=200)
