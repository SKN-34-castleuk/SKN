from django import forms  # Django Form 기능
from django.db import models  # Django Model 기능
from django.contrib.auth.models import User  # Django 기본 사용자 모델

class Question(models.Model):
    # 작성자 : 회원 삭제시 null 처리
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200)  # 질문 제목
    content = models.TextField()  # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일시 : 최초 자동 저장
    modified_at = models.DateTimeField(auto_now=True)     # 수정일시 : 수정시마다 자동 저장
    voters = models.ManyToManyField(User, related_name='question_votes')  # 질문 추천한 사람 목록

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 어떤 질문인지 연결 (질문 삭제시 삭제처리)
    content = models.TextField()  # 답변 내용
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voters = models.ManyToManyField(User, related_name='answer_votes')

# Django Model Form (정석적으로는 forms.py 작성하는게 원칙)
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # Question 모델 기반 폼 생성
        fields = ['subject', 'content']  # 폼에 포함될 필드
        labels = {
            'subject': '제목',  # subject 필드 출력 이름 설정
            'content': '내용',  # content 필드 출력 이름 설정
        }