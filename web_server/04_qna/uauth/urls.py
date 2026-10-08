from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Django 기본 인증 관련 View

app_name = 'uauth'

urlpatterns = [
    # 로그인 페이지
    path('login/', auth_views.LoginView.as_view(template_name = 'uauth/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),  # 로그아웃 처리
    path('signup/', views.signup, name='signup'),  # 회원가입 처리
    path('check_username/', views.check_username, name='check_username'),  # 아이디 중복 확인 처리
]