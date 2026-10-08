from django.shortcuts import render, redirect       # 템플릿 응답, 페이지 이동 처리
from .models import Question, Answer, QuestionForm  # 질문/답변 모델, 폼
from django.http import Http404, HttpResponseForbidden  # 404, 403 응답 처리
from django.core.paginator import Paginator         # 페이징 처리 도구
from django.contrib.auth.decorators import login_required  # 로그인 필요 데코레이터
from django.contrib import messages        # 사용자 알림 메시지 프레임워크
from django.shortcuts import resolve_url   # URL을 실제 경로로 변환
from django.http import JsonResponse       # JSON 응답 처리

# 질문 목록을 조회하고, 페이징 처리해서 목록 페이지를 반환하는 View
def index(request):
    # 답변 / 작성자를 함께 가져와 최신순 조회한 질문 객체
    questions = Question.objects.prefetch_related('answer_set').select_related('author').order_by('-created_at')
    
    # 페이징 처리
    page = request.GET.get('page', '1')  # 기본 페이지 1 설정
    paginator = Paginator(questions, 10)  # 페이지당 컨텐츠 수 지정
    page_obj = paginator.get_page(page)  # 현재 페이지 객체 생성
    return render(request, 'qna/index.html', {'page_obj': page_obj})  # 현재 목록 페이지 렌더링

# 질문 번호에 해당하는 상세 페이지를 조회하는 View
def question_detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)  # 해당 id의 질문객체 생성
        # print(f'{question = }')  # 필요시 logging
        return render(request, 'qna/question_detail.html', {'question': question})
    except Question.DoesNotExist:
        raise Http404('해당 질문은 존재하지 않습니다.')  # 질문이 없으면 404 처리

# 질문 작성 폼을 조회하고, 새 질문을 저장하는 View
@login_required(login_url='uauth:login')  # 로그인시 진행, 미로그인시 로그인페이지로 이동
def question_create(request):
    if request.method == 'POST':  # 폼 제출 요청이면
        form = QuestionForm(request.POST)  # POST 데이터로 폼 생성
        if form.is_valid():
            question = form.save(commit=False)  # DB 저장하지않고 Form 객체만 생성
            question.author = request.user      # 현재 로그인 사용자를 작성자로 지정
            question.save()  # DB 반영

            # 해당 질문 상세 페이지로 이동
            return redirect('qna:question_detail', question_id=question.id)
    else:
        form = QuestionForm()  # POST 이외 요청은 빈 폼 생성

    # 질문 작성 폼 렌더링
    return render(request, 'qna/question_form.html', {'form': form})

# 기존 질문을 수정할 수 있도록 처리하는 View
@login_required(login_url='uauth:login')
def question_modify(request, question_id):
    question = Question.objects.get(id=question_id)  # 수정할 원본 질문 객체

    # 수정권한 검사 : 작성자 본인 또는 관리자가 아니면 403 응답
    if request.user != question.author and not request.user.is_staff:
        return HttpResponseForbidden('수정권한이 없습니다.')

    # 수정 폼 제출한 경우
    if request.method == 'POST':
        # 기존 객체에 덮어쓰기용 폼 생성
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()  # 수정 내용 저장
            return redirect('qna:question_detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)  # 원본 데이터로 폼 객체 생성

    return render(request, 'qna/question_form.html', {'form': form})

# messages프레임워크 레벨
# - messages.success()  # 작업이 정상적으로 완료되었음을 사용자에게 알리는 성공 메시지
# - messages.error()  # 오류 발생 또는 권한 문제 등을 사용자에게 알리는 에러 메시지
# - messages.warning()  # 주의가 필요한 상황임을 알리는 경고 메시지
# - messages.info()  # 단순 정보나 안내 사항을 사용자에게 전달하는 메시지

# 질문 삭제 처리
@login_required(login_url='uauth:login')
def question_delete(request, question_id):
    question = Question.objects.get(id=question_id)  # 삭제할 원본 질문 객체

    # 삭제권한 검사 : 작성자 본인 또는 관리자가 아니면 403 응답
    if request.user != question.author and not request.user.is_staff:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('qna:question_detail', question_id= question_id)  # 상세페이지로 이동

    question.delete()  # 질문 삭제
    return redirect('qna:index')  # 메인페이지 이동

# 질문 추천을 추가하거나 취소하고, 결과를 json형식으로 반환하는 View
@login_required(login_url='uauth:login')
def question_vote(request, question_id):
    question = Question.objects.get(id=question_id)  # 삭제할 원본 질문 객체

    # 본인이 게시한 질문에는 좋아요 할수 없음
    if request.user == question.author:
        return JsonResponse({
            'result': 'error',
            'message': '본인이 작성한 글은 추천할 수 없습니다.'
        })
    # 현재 추천한 질문을 이미 내가 추천을 했으면
    if question.voters.filter(id=request.user.id).exists():
        question.voters.remove(request.user)  # 추천 취소
    else:
        question.voters.add(request.user)  # 추천하지 않은 사람은 추천인으로 추가

    # 결과와 추천수 반환
    return  JsonResponse({
        'result': 'success',
        'vote_count': question.voters.count()
    })

# 특정 질문에 대한 답변을 생성하는 View
@login_required(login_url='uauth:login')
def answer_create(request, question_id):
    content = request.POST.get('content')
    
    question = Question.objects.get(id=question_id)  # 해당 질문의 question 객체
    # 답변 DB 저장 및 답변 객체 생성
    answer = Answer.objects.create(question=question, content=content, author=request.user)
    print(f"{question_id}번 질문에 {answer.id}번 답변이 생성되었습니다.")

    # POST 요청 후에는 리다이렉트를 통해서 URL을 변경해줘야 새로고침 이슈를 회피할 수 있다.
    return redirect(f"{resolve_url("qna:question_detail", question_id=question_id)}#answer_{answer.id}")

# 답변 내용을 수정할 수 있도록 처리하는 View
@login_required(login_url='uauth:login')
def answer_modify(request, answer_id):
    question_id = request.GET.get('question_id')
    answer = Answer.objects.get(id=answer_id)  # 수정할 답변 객체

    # 수정권한 검사 : 작성자 본인 또는 관리자가 아니면 에러메시지 및 페이지 이동
    if request.user != answer.author and not request.user.is_staff:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)
    
    # 수정 폼 제출한 경우
    if request.method == 'POST':
        content = request.POST.get('content')
        answer.content = content  # 답변 내용 변경
        answer.save()             # 수정 내용 저장
        messages.info(request, '답변을 정상적으로 수행했습니다.')

        # 페이지 이동 : 수정한 답변 위치로 이동
        return redirect(f'{resolve_url('qna:question_detail', question_id=question_id)}#answer_{answer_id}')

# 답변 삭제 처리
@login_required(login_url='uauth:login')
def answer_delete(request, answer_id):
    question_id = request.GET.get('question_id')  # 본래 질문 번호
    answer = Answer.objects.get(id=answer_id)  # 삭제할 답변 객체

    # 삭제권한 검사 : 작성자 본인 또는 관리자가 아니면 403 응답
    if request.user != answer.author and not request.user.is_staff:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('qna:question_detail', question_id= question_id)  # 상세페이지로 이동

    answer.delete()  # 답변 삭제
    messages.success(request, '답변을 정상적으로 삭제했습니다.')
    return redirect('qna:question_detail', question_id = question_id)  # 상세페이지 이동

# 답변 추천을 추가하거나 취소하고, 결과를 json형식으로 반환하는 View
@login_required(login_url='uauth:login')
def answer_vote(request, answer_id):
    answer = Answer.objects.get(id=answer_id)  # 추천할 대상 답변 객체

    # 본인이 게시한 답변에는 좋아요 할수 없음
    if request.user == answer.author:
        return JsonResponse({
            'result': 'error',
            'message': '본인이 작성한 답변은 추천할 수 없습니다.'
        })

    # 현재 추천한 답변을 이미 내가 추천을 했으면
    if answer.voters.filter(id=request.user.id).exists():
        answer.voters.remove(request.user)  # 추천 취소
    else:
        answer.voters.add(request.user)  # 추천하지 않은 사람은 추천인으로 추가

    # 결과와 추천수 반환
    return  JsonResponse({
        'result': 'success',
        'vote_count': answer.voters.count()
    })