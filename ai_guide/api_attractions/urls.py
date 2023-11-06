from django.urls import path

from api_attractions.views import AttractionApiView, TextToVoiceConverterView

urlpatterns = [
    path('get_guide/', AttractionApiView.as_view(),),
    path('get_audio/<attraction_id>/', TextToVoiceConverterView.as_view()),
]
