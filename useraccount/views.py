from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import logging


from useraccount.forms import RegistrationForm, LoginForm, UserAccountUpdateForm
from useraccount.models import UserAccount

logger = logging.getLogger(__name__)

def landing_page_view(request):
    """
    Return site landing page
    :template:`useraccount/home.html`
    """
    return render(request, "useraccount/home.html")

def registration_view(request):
    """
    Register user.
    **Context**
    ``register_form``
        register form (email, password).
    **Template:**
    :template:`useraccount/register.html`
    """
    context = {}


    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            account = authenticate(email=email, username=email, password=raw_password)
            logger.info(f'New user {request} logged in => {request.user}')
            login(request, account)

            logger.warning(f'SUCCESSFUL log in new registration {request}')

            return redirect('home')
        else:
            logger.warning(f'FAILED registration {request}')
            context['registration_form'] = form
            return render(request, "useraccount/register.html", context)
    else: #get request
        context['registration_form'] = RegistrationForm()
        return render(request, "useraccount/register.html", context)

def login_view(request):
    """
    Log user in.
    **Context**
    ``login_form``
        login form (email, password ).
    **Template:**
    :template:`useraccount/login.html`
    """
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    context = {}

    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user:
                login( request, user)
                logger.info(f'SUCCESSFUL login - {request.user} | |  {request}')

                return redirect('home')
        else:
            context['login_form'] = form
            logger.warning(f'FAILED log in |  {form}')
            return render(request, 'useraccount/login.html', context)
    else:
        context['login_form'] = LoginForm()
        return render(request, 'useraccount/login.html', context)

@login_required(login_url='login')
def logout_view(request):
    """
    Destroys auth session`.
    Returns redirect to guest page home.html
    """
    logger.info(f'SUCCESSFUL log out - {request.user} | |  {request}')

    logout(request)
    return redirect('home')

@login_required(login_url='login')
def update_user_view(request):
    """
    Update an instance of :model:`useraccount.UserAccount`.
    **Context**
    ``update_form``
        update form with data from user.id:`useraccount.UserAccount`.
    **Template:**
    :template:`useraccount/profile.html`
    """
    context = {}

    if request.POST:
        form = UserAccountUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            logger.info(f'SUCCESSFUL user update - {request.user} | |  {request}')

            return redirect('home')
        else:
            form = UserAccountUpdateForm(initial={
                "email": request.user.email,
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone_number": request.user.phone_number,
            })

            logger.warning(f'FAILED user update - errors: {form.errors} | {request.user} | |  {request}')

        context["update_form"] = form
        return render(request, "useraccount/profile.html", context)
    else:
        form = UserAccountUpdateForm(initial={
            "email": request.user.email,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "phone_number": request.user.phone_number,
        })

        context['update_form'] = form
        return render(request, "useraccount/profile.html", context)


@login_required(login_url='login')
def network_view(request):
    """
    Display list of :model:`useraccount.UserAccount`.
    **Context**
    ``accounts``
        A list of instances:model:`useraccount.UserAccount`.
    **Template:**
    :template:`useraccount/network.html`
    """
    logger.info(f'{request.user} request network view.')

    context = {}

    accounts = UserAccount.objects.all()
    context['accounts'] = [
        {
            'first_name': account.first_name,
            'last_name': account.last_name,
            'phone_number': account.phone_number,
            'email': account.email,
            'username': account.username,
            'x': account.address_x,
            'y': account.address_y,
          } for account in accounts]

    return render(request, "useraccount/network.html", context)

@login_required(login_url='login')
def account_view(request, slug):
    """
    Display an individual :model:`useraccount.UserAccount`.
    **Context**
    ``account``
        An instance of :model:`useraccount.UserAccount`.
    **Template:**
    :template:`useraccount/network_account.html`
    """
    logger.info(f'{request.user} request network single account slug={slug}.')

    context = {}
    account = get_object_or_404(UserAccount, username=slug)
    context['account'] = account

    return render(request, "useraccount/network_account.html", context)






