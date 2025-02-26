from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

# Create your views here.

def home(request):
    categories = Category.objects.all()
    top_offers = Offer.objects.all()[:10]
    context = {"categories": categories, "top_offers": top_offers}
    return render(request, 'base/home.html', context)

def offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    context = {"offer": offer}
    return render(request, 'base/offer.html', context)

def category(request, pk):
    category = Category.objects.get(pk=pk)
    offers = category.offers.all()
    context = {'category': category, 'offers': offers}
    return render(request, 'base/category.html', context)

def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'base/profile.html', context)
