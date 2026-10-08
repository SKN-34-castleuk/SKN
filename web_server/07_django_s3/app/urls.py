from django.urls import path  # URL 패턴 등록 함수
from . import views

app_name = 'app'  # URL 네임스페이스

urlpatterns = [
    path('', views.upload_file, name='upload'),  
 
]