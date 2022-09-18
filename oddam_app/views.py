from django.db.models import Count, Sum
from django.shortcuts import render
from django.views import View

from oddam_app.models import Donation, Institution, Category


# Create your views here.

class LandingPage(View):
    def get(self, request):
        institutions_counter = Donation.objects.distinct('institution_id').count()
        bags_counter = Donation.objects.aggregate(Sum('quantity'))
        return render(request, 'index.html', {'institutions_counter': institutions_counter,
                                              'bags_counter': bags_counter})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')
