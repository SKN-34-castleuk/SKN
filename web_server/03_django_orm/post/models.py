# Django ORM에서 모델 클래스를 만들떄 사용하는 모듈
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)        # 최대 100자 문자열 필드
    content = models.TextField()                    # 긴 본문 내용을 저장할 텍스트 필드
    created_at = models.DateTimeField(auto_now_add=True)    # 최초 생성 시간 자동 저장 필드
    updated_at = models.DateTimeField(auto_now=True)        # 수정시마다 시간 자동 저장 필드

    # 객체를 출력시 제목문자열 출
    def __str__(self):
        return self.title