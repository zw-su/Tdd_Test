# coding = utf-8

from django.shortcuts import render, redirect
import sys
import uuid
from django.core.mail import send_mail
from django.contrib.auth import authenticate

from django.contrib.auth import login as auth_login, logout as auth_logout
from accounts.models import Token


def send_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving ui', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for myproject_lists',
        f"Use this link to log in:\n\n{url}",
        '344655096@qq.com',
        [email])
    return render(request, 'sent_email.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)  
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
