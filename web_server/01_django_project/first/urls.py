from django.urls import path    # URL 경로를 설정하는 함수
from . import views             # 현재 앱의 views 모듈


app_name = 'first'

urlpatterns = [
    path('', views.index, name='index'),    # /first/ 요청을 index 뷰와 연걸
    path('helloworld', views.helloworld, name='helloworld'),    # /first/helloworld 요청을 helloworld 뷰와 연결
]