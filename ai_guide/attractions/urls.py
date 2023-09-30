from django.urls import path

from .views import ApiAnswers

urlpatterns = [
    path('get_guide/', ApiAnswers.as_view(),)
]
