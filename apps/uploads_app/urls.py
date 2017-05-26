# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.uploads_app.views import list
from django.conf import settings
from django.conf.urls.static import static



app_name = 'uploads_app'
urlpatterns = [
    url(r'^list$', list, name='list')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
