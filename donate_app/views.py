from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import json
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from donate_app.models import Institution, Donation, Category


# Create your views here.


class LandingPage(View):
    def get(self, request):
        number_of_supported_institution = Institution.objects.all().count()  # czy to ma być liczba instytucji, czy ilość wszystkich wsparć
        sum_of_donated_quantity = Donation.objects.aggregate(
            Sum('quantity'))  # https://docs.djangoproject.com/en/3.0/topics/db/aggregation/
        fundations = Institution.objects.filter(type=1)
        paginator_fundations = Paginator(fundations, 1)
        page = request.GET.get('page')
        p_fundations = paginator_fundations.get_page(page)
        organizations = Institution.objects.filter(type=2)
        paginator_organizations = Paginator(organizations, 1)
        p_organizations = paginator_organizations.get_page(page)
        collections = Institution.objects.filter(type=3)
        paginator_collections = Paginator(collections, 1)
        p_collections = paginator_collections.get_page(page)  # https://docs.djangoproject.com/en/2.2/topics/pagination/
        return render(request, 'index.html', {"no_institution": number_of_supported_institution,
                                              "sum_quantity": sum_of_donated_quantity,
                                              "fundations": p_fundations,
                                              "organizations": p_organizations,
                                              "collections": p_collections})


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        new_donation = json.loads((request.POST.get('add_donation')))

        donation = Donation.objects.create(
            quantity=int(new_donation['no_of_bags']),
            institution=Institution.objects.get(id=(int(new_donation['institution_id'][0]))),
            address=new_donation['address']['street'],
            phone_number=new_donation['address']['phone'],
            city=new_donation['address']['city'],
            zip_code=new_donation['address']['postcode'],
            pick_up_data=new_donation['donation_reception']['date'],
            pick_up_time=new_donation['donation_reception']['time'],
            pick_up_comment=new_donation['donation_reception']['more_info'],
            user=request.user
        )

        donation.save()

        for cat in new_donation['categories_ids']:
            category = Category.objects.get(id=cat)
            donation.categories.add(category)

        donation.save()
        return redirect('/donationconfirm/')


class DonationConfirmation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class Profil(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user).filter(is_taken=False)
        archive_donations = Donation.objects.filter(user=request.user).filter(is_taken=True)
        number_of_donations = Donation.objects.filter(user=user).count()
        sum_of_donated_quantity = Donation.objects.filter(user=user).aggregate(Sum('quantity'))

        return render(request, 'profil.html', {'donations': donations, 'archive_donations': archive_donations,
                                               'number_of_donations': number_of_donations,
                                               'sum_of_donated_quantity': sum_of_donated_quantity})

    def post(self, request):
        donation_id = request.POST.get("donation_id")
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect(reverse('profil'))
