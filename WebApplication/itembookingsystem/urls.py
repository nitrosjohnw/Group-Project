"""itembookingsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from helloworld import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.home),
    path('home/', views.home , name='home'),
    path('login/',views.loginPage , name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('booking/',views.bookingPage , name='booking'),
    path('account/',views.accountPage , name='account'),
    path('logout/',views.userLogout , name='logout'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)