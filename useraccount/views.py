
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from useraccount.forms import RegistrationForm

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
            # login(request, account)
            # return "hello";

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
