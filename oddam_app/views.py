from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from oddam_app.models import Donation, Institution, Category


# Create your views here.

class LandingPage(View):
    def get(self, request):
        funds = Institution.objects.filter(type=1)
        ngos = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)
        institutions_counter = Donation.objects.distinct('institution_id').count()
        bags_counter = Donation.objects.aggregate(Sum('quantity'))
        return render(request, 'index.html', {'institutions_counter': institutions_counter,
                                              'bags_counter': bags_counter,
                                              'funds': funds,
                                              'ngos': ngos,
                                              'local_collections': local_collections})


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories,
                                             'institutions': institutions})


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            url = request.GET.get('next', reverse('base'))
            return redirect(url)
        return render(request, 'register.html', {'message2': "Podany użytkownik nie istnieje. Załóż konto."})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('base'))


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if name and surname and email and password == password2:
            User.objects.create_user(username=email, email=email, password=password, first_name=name, last_name=surname)
            return redirect(reverse('login'))
        else:
            return render(request, 'register.html',
                          {'name': name, 'surname': surname, 'email': email,
                           'message': "Nie uzupełniono wszystkich pól lub hasła nie są identyczne!"})
