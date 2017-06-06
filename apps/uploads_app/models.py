# -*- coding: utf-8 -*-
from django.db import models
from ..login_and_registration_app.models import User
import datetime


def get_upload_path(instance, filename):
    return  '{0}/{1}'.format(instance.user.email, filename)

class Document(models.Model):


    user = models.ForeignKey(User)
    #docfile = models.FileField(upload_to= 'documents/'+ user. + '%Y/%m/%d')
    #docfile = models.FileField(upload_to= '/'.join(['documents', '%Y','%m','%d' ,str(instance.pk), filename]))
    docfile = models.FileField(upload_to=get_upload_path)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __unicode__(self):
        return self.docfile.url
