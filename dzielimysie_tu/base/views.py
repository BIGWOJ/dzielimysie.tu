from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import My_User_Creation_Form

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

def login_page(request):
    page = 'login'

    # If user is already logged in, redirect to home page from login page
    if request.user.is_authenticated:
        return redirect('home_page')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        # password = request.POST.get('password')
        username = request.POST.get('username')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        # print(email, password)
        user = authenticate(request, username=username, email=email)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Email or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def register_page(request):
    page = 'register'
    form = My_User_Creation_Form()
    context = {'form': form, 'page': page}

    if request.method == 'POST':
        form = My_User_Creation_Form(request.POST)
        if form.is_valid():
            # Commit=false -> not saving to database yet, firstly clearing up data and logging up on the page
            user = form.save(commit=False)
            # user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong during registration')

    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home_page')

