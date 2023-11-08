from django.urls import path

from api_attractions.views import (AttractionApiView,
                                   TextToVoiceConverterApiView)

urlpatterns = [
    path('get_guide/', AttractionApiView.as_view(),),
    path('get_audio/<attraction_id>/', TextToVoiceConverterApiView.as_view()),
]
