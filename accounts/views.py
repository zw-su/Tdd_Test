# coding = utf-8

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token, User
from django.urls import reverse


def send_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + "?token=" + str(token.uid))
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        '你的待办事项登陆网址',
        message_body,
        '344655096@qq.com',
        [email])
    messages.success(
        request, "Check your email, we've sent you a link you can open")
    # messages.add_message(
    #   request,
    #   messages.SUCCESS,
    #   "Check your email, we've sent you a link you can open")
    return redirect(f'{url}')


def login(request):

    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')
