# excel_handler/urls.py

from django.urls import path
from . import views
from .views import display_excel_data

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('details/', views.excel_detail, name='excel_detail'),
    path('display-excel/', display_excel_data, name='display_excel_data'),
]
