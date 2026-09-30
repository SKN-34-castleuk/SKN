"""
URL configuration for _01_django_project project.

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
from django.contrib import admin                # Django 관리자 페이지 관련 기능
from django.urls import path, include           # URL 경로 설정 / 다른 앱 등의 urls.py 연결
from django.views.generic import RedirectView   # 특정 경로를 다른 URL로 이동시키는 제네릭 

urlpatterns = [
    path('admin/', admin.site.urls),    # /admin/ 주소로 요청이 들어오면 관리자 페이지로 이동
    path('',RedirectView.as_view(url='/first/', permanent=False)),  # 루트 주소 /로 요청이 들어오면 /first/로 이동 (임시 이동)
    path('first/',include('first.urls')),   # /first/ 주소로 시작하는 요청은 first 앱의 urls.py에서 처리
    path('second/',include('second.urls')),  # /second/ 주소로 시작하는 요청은 second 앱의 urls.py에서 처리
    path('third/',include('third.urls')),
]
