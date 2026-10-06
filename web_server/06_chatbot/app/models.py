from django.db import models

# 메시지 내역을 저장하는 모델
class ChatMessage(models.Model):
    session_id = models.CharField(max_length=255, db_index=True)  # 세션 ID : 인덱스 생성
    message_type = models.CharField(max_length=10, choices=[
        ('human', 'Human'),  # 사용자 메시지 타입
        ('ai', 'AI')         # AI 메시지 타입
    ])
    content = models.TextField()  # 메시지 본문 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 메시지 생성 시간 (생성시 자동 저장)

    def __str__(self):
        return f"{self.session_id} - {self.message_type}: {self.content[:50]}..."

    # 현재 모델 기본설정
    class Meta:
        ordering = ['created_at']  # 생성 시각 기준 오름차순 정렬