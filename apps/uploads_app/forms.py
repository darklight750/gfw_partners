# -*- coding: utf-8 -*-

from django import forms
#from uploads_app.models import Document


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
