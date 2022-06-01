"""helpsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('jquery/<slug:subject>/', jqeury_course),
    path('jquery/solved/<int:id>/', solved),

    path('admin/', admin.site.urls, name="admin"),
    path('', home, name="home"),
    path('school/<slug:school>/', index, name="school"),
    path('create/', create, name="create"),
    path('question/<int:id>/', question, name="question"),
    path('edit/<int:id>/', edit, name="edit"),
    path('download/<path:filename>/', download_file, name='download'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
