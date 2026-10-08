from django.contrib import admin  # Django 관리자 기능 import
from .models import UserDetail  # 관리자에 등록할 UserDetail 모델 import

admin.site.register(UserDetail)  # UserDetail 모델을 관리자 페이지에 등록