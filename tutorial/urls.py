from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url

import LAP.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LAP.views.home, name='home'),
    path('endPage/', LAP.views.endPage, name='endPage'),
    path('contactPage/', LAP.views.contactPage, name='contactPage'),
    path('download/', LAP.views.download, name='download')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
