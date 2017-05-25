# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.uploads_app.views import list
app_name = 'uploads_app'
urlpatterns = [
    url(r'^list$', list, name='list')
]
