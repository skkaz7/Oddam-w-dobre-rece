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
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


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
                          {'name': name, 'surname': surname, 'email': email, 'message': "Nie uzupełniono wszystkich pół lub hasła nie są identyczne!"})
