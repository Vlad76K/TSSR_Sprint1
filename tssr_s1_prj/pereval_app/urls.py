from django.urls import path

from .views import SubmitData, PerevalAddedUpdate, PerevalAddedDetail, PerevalAddedList

app_name = 'pereval_app'
urlpatterns = [
    path('submitData/', SubmitData.as_view()),
    path('object/<int:pk>', PerevalAddedDetail.as_view(), name='pereval_detail'),
    path('pereval_change/<int:pk>', PerevalAddedUpdate.as_view(), name='pereval_change'),
    path('pereval/', PerevalAddedList.as_view(), name='pereval'),
]
