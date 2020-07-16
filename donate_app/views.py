from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from donate_app.models import Institution, Donation


# Create your views here.


class LandingPage(View):
    def get(self, request):
        number_of_supported_institution = Institution.objects.all().count() #czy to ma być liczba instytucji, czy ilość wszystkich wsparć
        sum_of_donated_quantity = Donation.objects.aggregate(Sum('quantity')) #https://docs.djangoproject.com/en/3.0/topics/db/aggregation/
        return render(request, 'index.html', {"no_institution": number_of_supported_institution,
                                              "sum_quantity": sum_of_donated_quantity, })


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')
