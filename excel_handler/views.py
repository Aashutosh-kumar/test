# excel_handler/views.py

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import ExcelFile
from google.cloud import storage
from django.conf import settings
import openpyxl


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
        
        
        return redirect('display_excel_data')  

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

def display_excel_data(request):
    client = storage.Client.from_service_account_json(settings.GOOGLE_CLOUD_STORAGE_JSON_KEY_FILE)
    bucket = client.bucket(settings.GOOGLE_CLOUD_STORAGE_BUCKET)


    # List all blobs/files in the bucket
    blobs = list(bucket.list_blobs())
    print(blobs)
    # Sort blobs by creation time (most recent first)
    blobs.sort(key=lambda x: x.time_created, reverse=True)

    # Get the most recent blob (assumes at least one file exists)
    most_recent_blob = blobs[0]

    # Download the most recent blob to a local temporary location
    temp_file_path = 'most_recent_file.xlsx'
    most_recent_blob.download_to_filename(temp_file_path)

    # Read the contents of the downloaded file
    wb = openpyxl.load_workbook(temp_file_path)
    sheet = wb.active

    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)

    return render(request, 'display_excel_data.html', {'data': data})