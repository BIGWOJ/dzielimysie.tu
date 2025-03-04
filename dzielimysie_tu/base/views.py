from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Offer, User, Photo, Follow_user, Follow_offer
from .forms import My_User_Creation_Form, Offer_Form

# q = query

def not_done(request):
    return render(request, 'base/not_done_yet.html')

def home(request):
    categories = Category.objects.all()
    top_offers = Offer.objects.all()[:10]
    context = {"categories": categories, "top_offers": top_offers}

    # Filtering offers
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        offers = Offer.objects.filter(title__icontains=q)
        context['offers'] = offers

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

@login_required(login_url='login_page')
def follow_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    if request.user in offer.followers.all():
        offer.followers.remove(request.user)
    else:
        offer.followers.add(request.user)
    return redirect('offer_page', pk=pk)

@login_required(login_url='login_page')
def follow_user(request, pk):
    followed_user = User.objects.get(pk=pk)
    if request.user in followed_user.followers.all():
        followed_user.followers.remove(request.user)
    else:
        followed_user.followers.add(request.user)
    return redirect('user_profile_page', pk=pk)

@login_required(login_url='login_page')
def following(request, page):
    try:
        offers = Offer.objects.filter(followers=request.user)
    except Offer.DoesNotExist:
        offers = []

    try:
        followed_users = User.objects.filter(followers=request.user)
    except User.DoesNotExist:
        followed_users = []
    print(followed_users)
    context = {'offers': offers, 'page': page, 'followed_users': followed_users}
    return render(request, 'base/following.html', context)

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

def user_offers(request, pk):
    offers = Offer.objects.filter(creator=pk)
    user = User.objects.get(pk=pk)
    context = {'offers': offers, 'user': user}
    return render(request, 'base/user_offers.html', context)

def login_page(request):
    page = 'login'
    # If user is already logged in, redirect to home page from login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_message = False

        try:
            user = User.objects.get(email=email)
        except:
            error_message = True
            messages.error(request, 'Hasło albo mail jest niepoprawne')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            if not error_message:
                messages.error(request, 'Hasło albo mail jest niepoprawne')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def register_page(request):
    page = 'register'
    form = My_User_Creation_Form()
    
    context = {'register_form': form, 'page': page}

    if request.method == 'POST':
        form = My_User_Creation_Form(request.POST)
        if form.is_valid():
            # Commit=false -> not saving to database yet, firstly clearing up data and logging up on the page
            user = form.save(commit=False)
            # user.username = user.username
            user.save()
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Coś poszło nie tak. Spróbuj ponownie')

    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home_page')

# TO DO
def take_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    context = {'offer': offer}
    return render(request, 'base/take_offer.html', context)

# TO DO
def chat(request, pk):
    offer = Offer.objects.get(pk=pk)
    context = {'offer': offer}
    return render(request, 'base/chat.html', context)

@login_required(login_url='login_page')
def create_offer(request):
    form = Offer_Form(request.POST, request.FILES)
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            offer = form.save(commit=False)
            if offer.place == None:
                offer.place = "Nie podano"
            offer.creator = request.user

            offer.save()

            images = request.FILES.getlist('photos')
            if len(images) == 0:
                photo = Photo(offer=offer, photo='offer_photos/default_offer_photo.png')
                photo.save()
            else:
                for image in images:
                    photo = Photo(offer=offer, photo=image)
                    photo.save()
            return redirect('offer_page', pk=offer.id)

        else:
            messages.error(request, 'Coś poszło nie tak. Spróbuj ponownie')

    context = {'form': form, 'categories': categories}
    return render(request, 'base/create_offer.html', context)

@login_required(login_url='login_page')
def edit_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    form = Offer_Form(instance=offer)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = Offer_Form(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            if offer.place == None:
                offer.place = "Nie podano"
            offer.creator = request.user

            offer.save()

            current_photos = Photo.objects.filter(offer=offer)
            for photo in current_photos:
                photo.delete()

            images = request.FILES.getlist('photos')
            for image in images:
                photo = Photo(offer=offer, photo=image)
                photo.save()
            return redirect('offer_page', pk=offer.id)
        else:
            messages.error(request, 'Coś poszło nie tak. Spróbuj ponownie')

    context = {'form': form, 'categories': categories, 'offer': offer}
    return render(request, 'base/edit_offer.html', context)

@login_required(login_url='login_page')
def delete_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    if request.method == 'POST':
        offer.delete()
        return redirect('home_page')
    
    context = {'deleting_obj': offer}
    return render(request, 'base/delete_form.html', context)

 