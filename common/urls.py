from django.urls import path
from .views import (
    ReportStatusView,
    DownloadReportView, 
    GenerateReportView
)
urlpatterns = [
    path('reports/status/<str:task_id>/', ReportStatusView.as_view(), name='report-status'),
    path('reports/download/<str:filename>/', DownloadReportView.as_view(), name='report-download'),
    path('reports/generate/', GenerateReportView.as_view(), name='generate-report'),
]


