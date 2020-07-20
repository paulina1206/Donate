from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from donate_app.models import Institution, Donation


# Create your views here.


class LandingPage(View):
    def get(self, request):
        number_of_supported_institution = Institution.objects.all().count() #czy to ma być liczba instytucji, czy ilość wszystkich wsparć
        sum_of_donated_quantity = Donation.objects.aggregate(Sum('quantity')) #https://docs.djangoproject.com/en/3.0/topics/db/aggregation/
        fundations = Institution.objects.filter(type=1)
        paginator_fundations = Paginator(fundations, 1)
        page = request.GET.get('page')
        p_fundations = paginator_fundations.get_page(page)
        organizations = Institution.objects.filter(type=2)
        paginator_organizations = Paginator(organizations, 1)
        p_organizations = paginator_organizations.get_page(page)
        collections = Institution.objects.filter(type=3)
        paginator_collections = Paginator(collections, 1)
        p_collections = paginator_collections.get_page(page) #https://docs.djangoproject.com/en/2.2/topics/pagination/
        return render(request, 'index.html', {"no_institution": number_of_supported_institution,
                                              "sum_quantity": sum_of_donated_quantity,
                                              "fundations": p_fundations,
                                              "organizations": p_organizations,
                                              "collections": p_collections})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')
