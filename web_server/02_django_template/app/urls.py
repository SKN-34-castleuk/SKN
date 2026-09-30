from django.urls import path    # URL 경로를 설정하는 함수
from . import views             # 현재 앱의 views 모듈


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),    # /app/ 요청을 index 뷰와 연걸
    # /app/01_variables_filters 요청을 _01_variables_filters 뷰와 연결
    path('01_variables_filters', views._01_variables_filters, name='01_variables_filters'),    
    path('02_tags', views._02_tags, name='02_tags'),    
    path('03_layout', views._03_layout, name='03_layout'),    
]