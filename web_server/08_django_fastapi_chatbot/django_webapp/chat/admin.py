from django.contrib import admin  # Django 관리자 페이지 기능
from .models import ChatMessage  # ChatMessage 모델 가져오기


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """ChatMessage 모델의 관리자 페이지 설정"""
    
    list_display = ['id', 'session_id', 'message_type', 'content_preview', 'created_at']  # 목록 화면에 표시할 컬럼
    list_filter = ['session_id', 'message_type', 'created_at']  # 우측 필터 항목
    search_fields = ['content', 'session_id']  # 검색 가능 필드
    readonly_fields = ['created_at']  # 수정 불가능한 읽기 전용 필드
    ordering = ['-created_at']  # 최신순 정렬
    
    # 메시지 내용을 짧게 잘라서 미리보기로 보여주는 함수
    def content_preview(self, obj):
        """메시지 내용을 50자 기준으로 잘라 미리보기로 반환한다"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content  # 50자 초과 시 말줄임표 추가
    content_preview.short_description = '메시지 내용'  # 관리자 페이지 컬럼명
    
    # 관리자 페이지에서 새 채팅 메시지 추가를 막는 함수
    def has_add_permission(self, request):
        """관리자 페이지에서 직접 메시지를 추가하지 못하게 한다"""
        return False  # 추가 버튼 비활성화
    
    # 관리자 페이지 조회용 queryset을 반환하는 함수
    def get_queryset(self, request):
        """관리자 페이지에서 사용할 조회 객체를 반환한다"""
        return super().get_queryset(request).select_related()  # 연관 객체 조회 최적화