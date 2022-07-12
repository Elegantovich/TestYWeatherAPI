from django.urls import path

from .views import ReportView

app_name = 'api'

urlpatterns = [
    path('city/', ReportView.as_view()),
]
