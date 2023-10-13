from django.urls import path

from api_attractions.views import ApiAnswers

urlpatterns = [
    path('get_guide/', ApiAnswers.as_view(),),
]
