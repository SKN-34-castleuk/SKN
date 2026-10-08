from django import forms  # Django Form 기능
from django.db import models  # Django Model 기능
from django.contrib.auth.models import User  # Django 기본 사용자 모델
from django.contrib.auth.forms import UserCreationForm  # Django 기본 회원가입 폼

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User와 1:1로 매칭되는 유저 추가정보 모델
    birthday = models.DateField(null=True, blank=True)  # 생년월일, null 허용
    profile  = models.ImageField(upload_to='profiles/', null=True, blank=True)  #  프로필 이미지

class UserForm(UserCreationForm):
    birthday = forms.DateField(label='Birthday', required=False)  # 생년월일 입력 필드
    profile = forms.ImageField(label='Profile', required=False)   # 프로필 이미지 입력 필드

    class Meta:
        model = User  # User Model 기반 회원가입 폼
        fields = ['username', 'password1', 'password2', 'email']  # 회원가입 폼에 포함될 필드