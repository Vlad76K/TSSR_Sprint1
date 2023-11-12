from django.urls import path

from .views import SubmitData, PerevalGetAPIView, GetAllObjectsList, PerevalStatusGetAPIView, PerevalPatchAPIView, \
    PerevalCoordsGetAPIView, GetObjectsListByUserEmail

# PerevalAddedDetail, PerevalAddedUpdate, PerevalAddedList,

app_name = 'pereval_app'
urlpatterns = [
    path('submitData/', SubmitData.as_view(), name='submitdata'),
    path('list/submitData/', GetAllObjectsList.as_view()),
    path('get/submitData/<int:pk>', PerevalGetAPIView.as_view()),
    path('patch/submitData/<int:pk>', PerevalPatchAPIView.as_view()),
    path('get-status/submitData/<int:pk>', PerevalStatusGetAPIView.as_view()),
    path('get-coords/submitData/<int:pk>', PerevalCoordsGetAPIView.as_view()),
    path('get-useremail/submitData/', GetObjectsListByUserEmail.as_view()),
    # path('get-useremail/submitData/<str:email>', GetObjectsListByUserEmail.as_view()),

    # path('object/<int:pk>', PerevalAddedDetail.as_view(), name='pereval_detail'),
    # path('pereval_change/<int:pk>', PerevalAddedUpdate.as_view(), name='pereval_change'),
    # path('pereval/', PerevalAddedList.as_view(), name='pereval'),
]
