import json
import requests  # FastAPI 서버로 HTTP 요청 전송
from django.shortcuts import render  # 템플릿 렌더링
from django.http import JsonResponse  # Json 응답 객체
from django.views.decorators.csrf import csrf_exempt  # CSRF 검사 예외 처리
from django.conf import settings  # 프로젝트의 .settings.py
from .models import ChatMessage   # 채팅 메시지 모델


def chat_view(request):
    """채팅 화면 렌더링 — GET 파라미터로 session_id를 받아 이전 대화를 이어갈 수 있음"""
    session_id = request.GET.get('session_id')
    context = {'session_id': session_id} if session_id else {}  # 세션 id가 있으면 템플릿에 전달
    return render(request, 'chat/chat.html', context)


@csrf_exempt
def send_message(request):
    """사용자 메시지를 FastAPI로 전달하고, 응답을 DB에 저장"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST 요청만 허용됩니다'}, status=405)

    try:
        data = json.loads(request.body)  # 요청 본문 json 파싱
        user_message = data.get('message', '')  # 사용자 메시지 추출
        session_id = data.get('session_id', 'default')  # 세션 ID 추출

        # 사용자 메시지 없으면 400에러 응답
        if not user_message:
            return JsonResponse({'error': '메시지를 입력해주세요'}, status=400)

        # FastAPI 서비스로 메시지 전달
        fastapi_url = f"{settings.FASTAPI_SERVICE_URL}/chat/"
        response = requests.post(
            fastapi_url,
            json={'message': user_message, 'session_id': session_id},
            timeout=30
        )

        if response.status_code == 200:
            bot_response = response.json().get('response', '')  # AI 응답 추출

            # 사용자 메시지와 AI 응답을 DB에 저장
            ChatMessage.objects.create(session_id=session_id, message_type='human', content=user_message)
            ChatMessage.objects.create(session_id=session_id, message_type='ai', content=bot_response)

            return JsonResponse({'response': bot_response, 'status': 'success'})
        else:
            return JsonResponse({'error': 'FastAPI 서비스 오류', 'status': 'error'}, status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'연결 오류: {e}', 'status': 'error'}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식'}, status=400)


def get_history(request):
    """DB에서 대화 이력을 불러오고, FastAPI 세션에도 주입해 연속 대화를 지원"""
    session_id = request.GET.get('session_id', 'default')
    messages = ChatMessage.objects.filter(session_id=session_id)[:20]  # 최근 20개 메시지만 조회

    history = []
    service_history = []
    for msg in messages:
        history.append({
            'type': 'user' if msg.message_type == 'human' else 'bot',
            'message': msg.content,
            'timestamp': msg.created_at.isoformat()
        })
        # FastAPI 서비스에 전달할 LangChain 형식 이력
        service_history.append({
            'type': msg.message_type,
            'content': msg.content
        })

    # FastAPI 세션에 DB 이력 주입 (실패해도 화면 이력 반환은 계속)
    try:
        requests.post(
            f"{settings.FASTAPI_SERVICE_URL}/chat/history/set",  # 이력 설정 엔드포인트 주소
            json={'session_id': session_id, 'history': service_history},  # 세션 ID, 대화이력 전달
            timeout=15
        )
    # 이력 동기화 작업 실패시 무시하고 진행
    except requests.exceptions.RequestException:
        pass

    return JsonResponse({'history': history})  # 화면 표시용 이력 반환