from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

# q = query

def home(request):
    categories = Category.objects.all()
    top_offers = Offer.objects.all()[:10]
    context = {"categories": categories, "top_offers": top_offers}

    # Filtering offers
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        offers = Offer.objects.filter(title__icontains=q)
        context['offers'] = offers
        print(offers)
        return render(request, 'base/category.html', context)
    else:
        q = ''

    return render(request, 'base/home.html', context)

def offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    if offer.price == None:
        offer.price = "Za darmo"
    context = {"offer": offer}
    return render(request, 'base/offer.html', context)

def category(request, pk):
    category = Category.objects.get(pk=pk)
    offers = Offer.objects.filter(category=category)
    context = {'category': category, 'offers': offers}
    print(offers)
    # if request.GET.get('q') != None:
    #     q = request.GET.get('q')
    #     offers = Offer.objects.filter(category__icontains=q)
    #     context['offers'] = offers
    #     print(offers)
    #     return render(request, 'base/category.html', context)
    # else:
    #     q = ''

    return render(request, 'base/category.html', context)

def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'base/profile.html', context)
