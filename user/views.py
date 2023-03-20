from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def user(request, user_id):
    return render(request, 'user/user.html', {'title': user_id})


def sign_in(request):
    return render(request, 'user/sign_in.html', {'title': 'Signin page'})


def sign_out(request, user_id):
    return HttpResponseRedirect(reverse('home'))