from django.shortcuts import render, redirect       # 템플릿 응답, 페이지 이동 처리
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import UserForm, UserDetail
from django.db import transaction
from django.contrib.auth.models import User
from django.http import JsonResponse       # JSON 응답 처리

# 현재 로그인한 사용자를 로그아웃시키는 View
def logout(request):
    auth_logout(request)      # 세션 정보 삭제 및 로그아웃 처리
    return redirect('index')  # 메인페이지로 이동

# 회원가입 처리 후 추가정보 저장과 자동 로그인까지 수행하는 View
def signup(request):
    if request.method == 'POST':  # 회원가입 폼 제출 요청인 경우
        form = UserForm(request.POST, request.FILES)  # 일반 데이터와 파일 데이터를 가진 유저폼
        if form.is_valid():
            with transaction.atomic():  # 트랜잭션을 통해 user, user_detail을 트랜잭션으로 처리
                user = form.save(commit=True)  # 유저 객체생성 + DB저장

                user_detail = UserDetail(
                    user = user,
                    birthday = form.cleaned_data.get('birthday'),  # 폼의 정제된 생년월일 데이터
                    profile = form.cleaned_data.get('profile'),    # 폼의 정제된 프로필 데이터
                )
                user_detail.save()  # 유저상세정보 DB 저장
            print(f"회원가입 완료되었습니다. {user_detail}")

            # 회원가입 후 로그인 처리
            username = form.cleaned_data.get('username')  # 입력한 아이디
            raw_password = form.cleaned_data.get('password1')  # 입력한 비밀번호
            user = authenticate(username = username, password=raw_password)  # 사용자 인증
            auth_login(request, user)  # 인증된 사용자로 로그인
            return redirect('index')   # 인덱스 페이지로 이동
    else:
        form = UserForm()  # GET 요청이면 빈 회원가입 폼 생성

    return render(request, 'uauth/signup.html', {'form': form})

# 전달받은 username의 중복 여부를 JSON으로 반환하는 함수
def check_username(request):
    username = request.GET.get('username')  # GET요청 파라미터에서 username 값 추출
    is_exists = User.objects.filter(username=username).exists()  # 동일한 username 존재 여부 확인

    # 존재하면 사용불가 / 없으면 사용 가능 응답
    if is_exists:
        return JsonResponse({'available': False, 'message': '이미 사용중인 아이디입니다.'})
    return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})
