from django.shortcuts import render, redirect
from django.contrib import messages

from .aws_s3_service import S3Client
from .models import FileUploadForm

s3_client = S3Client()

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            print(model.file)
            obj_url = s3_client.upload(form.files['file'])
            print(obj_url)
            model.file = obj_url
            model.save()

            messages.success(request, f"""
            <a href = "{obj_url}"> 업로드한 파일 </a>을 확인하세요!
            """)

            return redirect('app:upload')
    else:
        form = FileUploadForm()
    return render(request, 'app/upload.html', {'form': form})