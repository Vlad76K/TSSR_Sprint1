from django.urls import path

from .views import SubmitData

app_name = 'pereval_app'
urlpatterns = [
    path('submitData/', SubmitData.as_view()),
]
