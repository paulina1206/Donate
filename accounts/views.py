from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from accounts.form import RegisterForm


# Create your views here.


# class Register(View):
#     def get(self, request):
#         return render(request, 'register.html')
#     def post(self, request):
#         name = request.POST['name']
#         surname = request.POST['surname']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#         if password != password2:
#             massage = "Password must be identical"
#             return render(request, 'register.html', {'massage':massage})
#         else:
#             User.objects.create_user(username=email, password= password, email=email, first_name=name, last_name=surname)
#             return redirect('/login/')


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")
