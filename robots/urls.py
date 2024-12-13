from django.urls import path
from .views import *

urlpatterns = [
    path('create/', RobotCreateView.as_view(), name='robot-create'),
    path('report/', RobotReportView.as_view(), name='robot-report'),
]
