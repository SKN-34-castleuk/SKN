from django.contrib import admin      # Django 관리자 기능
from .models import Question, Answer  # 등록할 모델들

admin.site.register(Question)
admin.site.register(Answer)