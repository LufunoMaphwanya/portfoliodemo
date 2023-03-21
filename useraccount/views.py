import urllib

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import urllib.request

import ipinfo

from portfolio_demo import settings
from useraccount.forms import RegistrationForm, LoginForm

def landing_page_view(request):
    return render(request, "useraccount/home.html")

def registration_view(request):
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            print("if form is valid")
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            account = authenticate(email=email, username=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
            print("else form.isvalid")
            print(form.errors)
            return render(request, "useraccount/register.html", context)
    else: #get request
        context['registration_form'] = RegistrationForm()
        print("else GET")
        return render(request, "useraccount/register.html", context)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user:
                login( request, user)
                return redirect('home')
        else:
            print("invalid")
            print(form.errors)
            context['login_form'] = form
            return render(request, 'useraccount/login.html', context)
    else:
        context['login_form'] = LoginForm()
        return render(request, 'useraccount/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

