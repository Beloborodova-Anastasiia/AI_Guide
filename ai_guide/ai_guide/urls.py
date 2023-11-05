from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_attractions.urls')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        path('__debug__/', include(debug_toolbar.urls)),
    )
