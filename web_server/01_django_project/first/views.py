from django.shortcuts import render     # 템플릿을 렌더링할때 사용
from django.http import HttpResponse    # 문자열 응답 반환

# /first/ 요청시 응답반환 View
def index(request):
    print(type(request))    # 자료형 확인
    print(request)          # 요청 정보
    return HttpResponse('Hello django') # 브라우저에 응답 반환

# /first/helloworld 요청시 응답반환 View
def helloworld(request):
    return HttpResponse("HELLO WORLD!!")

