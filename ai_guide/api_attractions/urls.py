from django.urls import path

from api_attractions.views import ApiAnswers, GetAudio

urlpatterns = [
    path('get_guide/', ApiAnswers.as_view(),),
    path('get_audio/<id>/', GetAudio.as_view()),
]
