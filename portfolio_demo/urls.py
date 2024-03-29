"""portfolio_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from useraccount.views import landing_page_view, registration_view, login_view, logout_view, update_user_view, network_view, account_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name="home"),
    path('register', registration_view, name="register"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('profile', update_user_view, name="profile"),
    path('network', network_view, name="network"),
    path('network/<slug>', account_view, name="account"),

]
