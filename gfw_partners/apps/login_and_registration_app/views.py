# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def store_to_session(request):
    request.session['register_first_name']=request.POST['first_name']
    request.session['register_last_name']=request.POST['last_name']
    request.session['register_email']=request.POST['email']
    return

def update_login_session(login,request):
    # Used during login and registration to 'login' the user
    # by storing the 'id','first_name','email' in session
    request.session['id']=login.id
    request.session['first_name']=login.first_name
    request.session['email']=login.email
    return

def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'login_and_registration_app/index.html', context)

def registration(request):

    if request.method == 'POST':
        print request.POST
        valid,data = User.objects.validate_and_register(request.POST)

        if valid == False:
            for err in data:
                messages.error(request,err)
                store_to_session(request);
            return redirect('/')

            # Now update session with the new registration values.
    update_login_session(data,request)


    return redirect('uploads_app:list')


def login(request):
    if request.method == 'POST':
        request.session.clear()
        valid, data = User.objects.validate_and_login(request.POST)

        if valid == False:
            for err in data:
                messages.error(request,err)
            return redirect('/')

    update_login_session(data,request)
    context = {
        'users': User.objects.all()


    }
    '''a = User.objects.all()
    for user in a:
        context[user] = []
        context['keys'].append(user)
        b = user.document_set.all()
        for doc in b:
            context[user].append(doc)
    print context'''

    for user in context['users']:
        for doc in user.document_set.all():
            print doc, 1
    if data.email == 'admin@admin.com':
        return render(request, 'login_and_registration_app/admin.html', context)

    return redirect('uploads_app:list')

def update_account_info(request):

    print request.method

    if request.method=='POST':
        print request.POST
        print request.session['id']
        context = {
            'user': User.objects.get(id=request.session['id'])
        }
        result = User.objects.update_user_info(request.POST, request.session['id'])
        if not result[0]:
            for error in result[1]:
                messages.error(request, error)

            # Redisplay the form again to display error messages and try again
            return render(request, "login_and_registration_app/update.html",context)

        # Appointment updated successfully
        return redirect('uploads_app:list')

    else:


        # Find the appointment and store info in context. We'll pass it to
        # the form, displaying current values in form.
        context = {
            "user": User.objects.get(id=request.session['id']),
        }
        print context

        # Render the form, passing the current appointment info in context.
        return render(request, "login_and_registration_app/update.html",context)


def logout(request):
    print "logout route"
    print "***********"
    request.session.clear()
    return redirect('/')
