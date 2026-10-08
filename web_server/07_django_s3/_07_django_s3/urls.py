"""
URL configuration for _07_django_s3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path,include    # URL 등록, URL 연결
from django.views.generic import RedirectView   # 특정경로 리다이렉트 View
urlpatterns = [
    path('', RedirectView.as_view(url='/app/')),    # /경로 접속시 /app/ 이동
    path('app/', include('app.urls')),      # app/... 접속시 app앱의 urls.py
]
