from django.shortcuts import render     # 템플릿을 렌더링할때 사용
from django.http import HttpResponse    # 문자열 응답 반환

# /third/ 요청시 응답반환 View
def index(request):
    return render(request, 'third/index.html')


# /third/good 요청시 응답반환 View
def good(request):
    return HttpResponse("good BOY")

