# excel_handler/views.py

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import ExcelFile
from google.cloud import storage

def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Initialize Google Cloud Storage client
        client = storage.Client()
        bucket = client.bucket('for-excel-files')  # Replace 'your-bucket-name' with your actual bucket name
        
        # Upload the file to Google Cloud Storage
        blob = bucket.blob(file.name)
        blob.upload_from_file(file)
        
        # Optionally, save file details in your database
        
        return redirect('excel_detail')
    else:
        form = ExcelUploadForm()
    return render(request, 'upload_excel.html', {'form': form})

def excel_detail(request):
    excel_files = ExcelFile.objects.all()
    paginator = Paginator(excel_files, 10)  # Show 10 Excel files per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'excel_detail.html', {'page_obj': page_obj})
