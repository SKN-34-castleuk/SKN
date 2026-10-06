from django.shortcuts import render, redirect
from datetime import datetime

# 메인 페이지를 화면에 출력하는 View
def index(request):
   return render(request, 'app/index.html')

# 세션에 여러 종류의 데이터를 저장하는 View
def set_session(request):
    # 세션 객체에 데이터 저장
    username = request.POST.get('username') # 시용자 username 입력값 가져오기
    request.session['username'] = username  # username 세션 저장

    # 모든 타입의 정보 저장 테스트
    request.session['point'] = 123456789    # 정수형
    request.session['prob'] = 0.123456      # 실수형
    request.session['expired'] = True       # Boolean
    request.session['nums'] = [1,2,3,4,5]   # 리스트
    request.session['data'] = {             # 딕셔너
        'message': 'Hello Django Session!!',
        'today' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return redirect('app:index')    # 저장 완료 후 메인페이지 이동
    
    

# 기존 세션 값을 수정하거나 삭제하는 View
def modify_session(request):
    # 새 속성을 추가/삭제
    # - 세션 객체의 최상위 키 변경은 자동으로 감지
    # - 중첩된 속성 변경시에는 명시적으로 변경됨을 설정해야 함
    request.session['favorite_color'] = 'springgreen'   # 세션 데이터 추가
    request.session['nums'].append(999)     # 리스트 데이터 추가
    request.session['data']['new_item'] = '새로운 아이템'     # 딕셔너리 데이터 추가

    request.session.modified = True     # 세션 변경사항 저장

    request.session.pop('point', None)    # point 세션 데이터 삭제 (없으면 무시)

    return redirect('app:index')

# 현재 세션 전체를 삭제하는 View
def delete_session(request):
    request.session.flush()     # 세션 데이터와 세션 쿠키를 모두 삭
    return redirect('app:index')

# 사용자가 입력한 이름과 값으로 쿠키를 생성하는 View
# - 쿠키는 response 객체에서 설정
def set_cookie(request):
    name = request.POST.get('cookie_name')  # 쿠키 이름 입력값
    value = request.POST.get('cookie_value')    # 쿠키 값 입력값

    response = redirect('app:index')    # 응답 객체 생성
    response.set_cookie(    
        name, value,    # 쿠키 이름과 값
        path = '/app/', # 해당 하위 경로 요청에서만 쿠키 전송
        max_age=120,    # 쿠키 유지시간 120초 
        httponly=True,  # js에서 접근 불가 (XSS 공격 방어)
        samesite='Lax', # CSRF 방어 : 외부 사이트에서 전송할떄는 쿠키 전송안합
        secure= False,  # HTTPS 전용 여부 (개발환경에서는 False => HTTP)
    )

    return response     # 쿠키가 담긴 응답 반환

# 지정한 이름의 쿠키를 삭제하는 View
def delete_cookie(request):
    response = redirect('app:index')    # 응답 객체 생성
    name = request.POST.get('cookie_name')  # 사용자 요청에서 cookie_name 값 (삭제할 쿠키 이름)
    response.delete_cookie(name, path='/app/')  # /app/ 경로 기준으로 해당 name 쿠키 삭제
    return response # 삭제 응답 반환