# excel_handler/views.py

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import ExcelFile
from google.cloud import storage
from django.conf import settings


def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Initialize Google Cloud Storage client using the provided JSON key file
        client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_STORAGE_JSON_KEY_FILE)

        # Get the GCS bucket
        bucket = client.bucket(settings.GOOGLE_CLOUD_STORAGE_BUCKET)

        # Upload the file to Google Cloud Storage
        blob = bucket.blob(file.name)
        blob.upload_from_file(file)
        
        
        return redirect('excel_detail')  

    else:
        # If the request method is not POST or no file is provided, render the form
        form = ExcelUploadForm()  # Make sure to replace 'ExcelUploadForm' with the actual form class
        return render(request, 'upload_excel.html', {'form': form})

def excel_detail(request):
    excel_files = ExcelFile.objects.all()
    paginator = Paginator(excel_files, 10)  # Show 10 Excel files per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'excel_detail.html', {'page_obj': page_obj})
