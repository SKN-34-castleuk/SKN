from django.shortcuts import render     # 템플릿을 렌더링할때 사용

# /second/ 요청시 응답반환 View
def index(request):
    return render(request, 'second/index.html')

