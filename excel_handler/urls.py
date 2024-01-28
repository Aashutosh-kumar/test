# excel_handler/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('details/', views.excel_detail, name='excel_detail'),
]
