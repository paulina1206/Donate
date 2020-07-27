"""donate URL Configuration

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
from django.contrib import admin
from django.urls import path
from donate_app import views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('adddonation/', views.AddDonation.as_view(), name='add_donation'),
    path('donationconfirm/', views.DonationConfirmation.as_view(), name='donation_confirmation'),
    path('profil/', views.Profil.as_view(), name='profil'),
]
