from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


import LAP.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LAP.views.home, name='home'),
    path('loadingPage/', LAP.views.loadingPage, name='loadingPage'),
    path('endPage/', LAP.views.endPage, name='endPage'),
    path('contactPage/', LAP.views.contactPage, name='contactPage'),
    path('upload/', LAP.views.upload, name='upload')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
