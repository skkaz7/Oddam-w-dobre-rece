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
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        categories = request.POST.getlist('categories')
        bags = request.POST.get('bags')
        organization_id = request.POST.get('organization')
        institution = Institution.objects.get(pk=organization_id)
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        data = request.POST.get('data')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')
        user = request.user
        instance = Donation.objects.create(quantity=bags, institution=institution, address=address,
                                           phone_number=phone, city=city, zip_code=postcode, pick_up_date=data,
                                           pick_up_time=time, pick_up_comment=more_info, user=user)
        for cat in categories:
            instance.categories.add(cat)
        return redirect(reverse('form-confirmation'))


class AddDonationConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


def get_inst_by_cat(request):
    type_ids = request.GET.getlist('type_ids')
    if type_ids is not None:
        institutions = Institution.objects.filter(categories__in=type_ids).distinct()
    else:
        institutions = Institution.objects.all()
    return render(request, "api_institutions.html", {'institutions': institutions})


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


class UserDetails(View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user_id=user.id)
        return render(request, 'user-details.html', {'user': user, 'donations': donations})

    def post(self, request):
        confirm = request.POST.get('confirm')
        donation = Donation.objects.get(id=confirm)
        donation.is_taken = True
        donation.save()
        return redirect(reverse('user-details'))


class UserUpdate(View):
    def get(self, request):
        user = request.user
        return render(request, 'user-update.html', {'user': user})

    def post(self, request):
        user = request.user
        if user.check_password(request.POST.get('password')):
            user.first_name = request.POST.get('name')
            user.last_name = request.POST.get('surname')
            user.email = request.POST.get('email')
            user.username = request.POST.get('email')
            user.save()
            return redirect(reverse('user-details'))
        return render(request, 'user-update.html', {'user': user, 'message': "Wprowadzono niepoprawne hasło!"})


class ChangePassword(View):
    def get(self, request):
        return render(request, 'change-password.html')

    def post(self, request):
        user = request.user
        if user.check_password(request.POST.get('old-password')):
            new_password = request.POST.get('new-password')
            new_password2 = request.POST.get('new-password2')
            if new_password == new_password2:
                user.set_password(new_password)
                user.save()
                return redirect(reverse('login'))
            return render(request, 'change-password.html', {'message2': "Nowe hasła nie są takie same!"})
        return render(request, 'change-password.html', {'message': "Stare hasło jest błędne!"})
