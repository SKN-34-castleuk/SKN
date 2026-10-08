from django.db import models
from django.utils import timezone


class ChatMessage(models.Model):
    """대화 메시지를 저장하는 모델 (human/ai 각각 별도 row)"""
    MESSAGE_TYPE_CHOICES = [
        ('human', 'Human'),  # 사용자 메시지 타입
        ('ai', 'AI')         # AI 메시지 타입
    ]

    session_id = models.CharField(max_length=255, db_index=True)   # 세션 식별자
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)  # 'human' or 'ai'
    content = models.TextField()                                     # 메시지 내용
    created_at = models.DateTimeField(default=timezone.now)         # 생성 시각

    class Meta:
        ordering = ['created_at']   # 시간 오름차순 정렬

    def __str__(self):
        return f"{self.session_id} - {self.message_type}: {self.content[:50]}"