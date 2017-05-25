# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.uploads_app.models import Document
from apps.uploads_app.forms import DocumentForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'],user_id=request.session['id'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('uploads_app:list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    print 1
    print 2
    print documents
    for i in documents:
        print i
    return render(
        request,
        'list.html',
        {'documents': documents.filter(user_id=request.session['id']), 'form': form}
    )
