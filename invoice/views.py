from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Household, Invoice

# Create your views here.


def household_list(request):
	homes = Household.objects.all()
	return render(request, 'invoice/household_list.html', {"homes": homes})

