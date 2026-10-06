import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, Http404
from django.shortcuts import render
from .models import ChatMessage
from .chatbot_service import get_by_session_id, invoke_chain_with_history

# 메인 페이지 렌더링 View
def index(request):
    return render(request, 'app/index.html')

# 새 대화에 사용할 고유한 session_id를 생성해 반환하는 View
@csrf_exempt   # CSRF 토큰 인증 비활성화
@require_POST  # POST 방식 요청처리
def init_conversation(request):
    session_id = str(uuid.uuid4())  # UUID 기반 고유 세션 ID 생성
    return JsonResponse({
        'session_id': session_id
    })

# 사용자의 질문을 받아 대화 이력을 포함한 챗봇 응답을 반환하는 View
@csrf_exempt
@require_POST
def chatbot(request):
    session_id = request.POST.get('session_id')  # 요청 데이터에서 session_id 추출
    print(session_id)
    query = request.POST.get('query')  # 사용자 질문 추출

    if not session_id or not query:
        return HttpResponseBadRequest('세션ID나 질문사항이 필수입니다!')  # 필수값 누락시 400 응답

    response = invoke_chain_with_history(session_id, query)  # 대화 이력을 반영해 챗봇 응답
    return JsonResponse({
        'content': response.content  # 챗봇 응답 내용 json 반환
    })

# 특정 세션의 대화 이력을 삭제하는 View
@csrf_exempt
@require_http_methods(['DELETE'])  # DELETE 방식 요청처리
def remove_conversation(request):
    try:
        body = json.loads(request.body)  # JSON 문자열 -> Python dict/list 변환
        session_id = body.get('session_id')  # 삭제할 session_id 추출
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Json Body 형식에 맞지 않습니다!')  # json 형식 오류시 400 응답

    if not ChatMessage.objects.filter(session_id=session_id).exists():  # 해당 session_id 미존재시
        raise Http404('Session ID를 찾지 못했습니다.')   # 404 에러 발생

    history = get_by_session_id(session_id)  # 세션별 대화 이력 객체 조회
    history.clear()  # 해당 세션의 대화 이력 삭제

    return JsonResponse({
        'result': 'success',
        'message': f"세션 ID {session_id}의 대화 이력 삭제 완료!"
    })

# 저장된 대화 세션 목록을 집계해서 반환하는 View
@require_GET
def get_session_list(request):
    from django.db.models import Min, Max, Count

    sessions = ChatMessage.objects.values('session_id').annotate(
        first_message_time = Min('created_at'),  # 세션별 첫 메시지 시각
        last_message_time = Max('created_at'),   # 세션별 마지막 메시지 시각
        messages_count = Count('id'),  # 세션별 메시지 개수
    )

    session_list = []
    for session in sessions:
        # 각 세션의 첫 메시지 조회
        first_message = ChatMessage.objects.filter(session_id=session['session_id']).first()

        session_list.append({
            'session_id': session['session_id'],
            'first_message_preview': first_message.content,  # 첫 메시지 내용(미리보기용)
        })

    return JsonResponse({
        'sessions': session_list,             # 세션 목록
        'total_sessions': len(session_list),  # 전체 세션 개수
    })

# 저장된 세션의 대화 내용을 다시 불러오는 View
@csrf_exempt
@require_POST
def restore_conversation(request):
    try:
        body = json.loads(request.body)  # 요청 본문 JSON 파싱
        session_id = body.get('session_id')  # session_id 추출
    except json.JSONDecodeError:
        return HttpResponseBadRequest('잘못된 JSON 형식입니다!')  # JSON 형식 오류시 400 응답

    if not ChatMessage.objects.filter(session_id=session_id).exists():
        return HttpResponseNotFound('세션이 존재하지 않습니다!')  # 해당 세션이 없으면 404 응답

    history = get_by_session_id(session_id)  # 해당 세션의 대화 내용 조회
    conversation_history = []
    for message in history.messages:
        conversation_history.append({
            'type': message.type,   # 메시지 유형
            'content': message.content  # 메시지 내용
        })

    return JsonResponse({
        'session_id': session_id,                      # 해당 대화의 Session_id
        'conversation_history': conversation_history,  # 대화 이력
        'message_count': len(conversation_history)     # 대화 개수
    })