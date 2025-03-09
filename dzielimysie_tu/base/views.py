from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Offer, User, Photo, Take_offer
from .forms import My_User_Creation_Form, Offer_Form

# q = query

def not_done(request):
    return render(request, 'base/not_done_yet.html')

def home(request):
    categories = Category.objects.all()
    top_offers = Offer.objects.all()[:5]
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
    
    user_is_taker = Take_offer.objects.filter(offer=offer, taker=request.user).exists()
    context = {"offer": offer, 'user_is_taker': user_is_taker}
    return render(request, 'base/offer.html', context)

def offers(request, offers_layout):
    offers = Offer.objects.all()
    context = {"offers": offers, 'offers_layout': offers_layout}
    return render(request, 'base/offers_page.html', context)

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

    context = {'offers': offers, 'page': page, 'followed_users': followed_users}
    return render(request, 'base/following.html', context)

def category(request, pk):
    category = Category.objects.get(pk=pk)
    offers = Offer.objects.filter(category=category)
    context = {'category': category, 'offers': offers}

    return render(request, 'base/category.html', context)

def user_profile(request, pk):  
    user = User.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login_page')
def user_settings(request):
    user = request.user

    if request.method == 'POST':
        # Changing password
        if 'current_password' in request.POST:
            password = request.POST.get('current_password')
            if user.check_password(password):
                password1 = request.POST.get('new_password')
                password2 = request.POST.get('new_password_confirm')
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    login(request, user)
                else:
                    messages.error(request, 'Nowe hasła nie są zgodne')
            else:
                messages.error(request, 'Obecne hasło jest niepoprawne')

        # Changing email
        elif 'new_email' in request.POST:
            new_email = request.POST.get('new_email')
            if new_email != user.email:
                user.email = new_email
                user.save()
                login(request, user)
            else:
                messages.error(request, 'Nowy email jest taki sam jak obecny')

        # Changing notifications
        elif 'new_message_notification' in request.POST or 'price_change_notification' in request.POST or 'new_offer_notification' in request.POST:
            user.new_message_notification = request.POST.get('new_message_notification') == 'on'
            user.price_change_notification = request.POST.get('price_change_notification') == 'on'
            user.new_offer_notification = request.POST.get('new_offer_notification') == 'on'

            user.save()
            messages.success(request, 'Powiadomienia zostały zapisane')
        
        # Changing avatar
        elif 'new_avatar' in request.FILES:
            avatar = request.FILES.get('new_avatar')
            user.avatar = avatar
            user.save()
            messages.success(request, 'Zdjęcie profilowe zostało zmienione')

        # Deleting account
        elif 'delete_account_password' in request.POST:
            password = request.POST.get('delete_account_password')
            password_confirm = request.POST.get('delete_account_password_confirm')
            if password == password_confirm and user.check_password(password):
                user.delete()
                messages.success(request, 'Konto zostało usunięte')
                return redirect('home_page')
            else:
                messages.error(request, 'Hasła nie są zgodne lub obecne hasło jest niepoprawne')

    context = {'user': user}
    return render(request, 'base/user_settings.html', context)

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

    context = {'register_form': form, 'page': page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home_page')

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
            offer.status = 'waiting'
            offer.save()

            images = request.FILES.getlist('photos')
            if len(images) == 0:
                photo = Photo(offer=offer, photo='offer_photos/default_offer_photo.png')
                photo.save()
            else:
                for image in images:
                    photo = Photo(offer=offer, photo=image)
                    photo.save()
            return redirect('offer_page', offer.id)

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

 # TO DO

def my_offers(request, status):
    offers = Offer.objects.filter(creator=request.user)
    offers_statuses = Offer.statuses
    taked_offers_statuses_dict = dict(Take_offer.statuses)
    
    taked_offers = Take_offer.objects.filter(taker=request.user)
    offers_filtered = offers.filter(status=status)

    # __ allows to access the attributes of related models in the query
    # Need of Q usage cause of tuple distinct issues
    offers_created_with_takers_pending= [
        (offer, Take_offer.objects.filter(status='waiting'), User.objects.filter(Q(take_offer__offer=offer) & Q(take_offer__status='waiting')).distinct())
        for offer in offers
    ]
    
    offers_taked_with_taker_pending = [
        (take_offer.offer, take_offer.status, User.objects.filter(take_offer__status='waiting', take_offer__taker=request.user))
        for take_offer in taked_offers
    ]
    offers_with_takers_pending = offers_created_with_takers_pending + offers_taked_with_taker_pending
    
    # print('created', offers_created_with_takers_pending,'\n')
    # print('taked', offers_taked_with_taker_pending)
    # print(offers_with_takers_waiting)

    offers_created_with_takers_accepted = [(offer, Take_offer.objects.filter(status='accepted', offer__creator=request.user)) for offer in offers_filtered]

    offers_taked_with_takers_accepted = [(take_offer.offer, Take_offer.objects.filter(status='accepted', offer=take_offer.offer)) for take_offer in taked_offers]

    offers_with_takers_accepted = offers_created_with_takers_accepted + offers_taked_with_takers_accepted

    print('accepted', offers_with_takers_accepted)

    # offers_created_with_takers_accepted = [
    #     (offer, Take_offer.objects.filter(status='accepted'), User.objects.filter(Q(take_offer__offer=offer) & Q(take_offer__status='accepted')).distinct())
    #     for offer in offers
    # ]
    
    # offers_taked_with_taker_accepted = [
    #     (take_offer.offer, take_offer.status, User.objects.filter(take_offer__status='accepted', take_offer__taker=request.user))
    #     for take_offer in taked_offers
    # ]

    # offers_with_takers_accepted = offers_created_with_takers_accepted + offers_taked_with_taker_accepted

    # print('created', offers_created_with_takers_accepted)
    # print('taked', offers_taked_with_taker_accepted)

    # offers_with_takers_accepted = [(offer, User.objects.filter(take_offer__offer=offer, take_offer__status='accepted')) for offer in offers]
    
    offers_with_takers_cancelled = [(offer, User.objects.filter(take_offer__offer=offer, take_offer__status='cancelled')) for offer in offers]
    
    context = {
        'offers_filtered': offers_filtered,
        'offers_status': status,
        'offers_statuses': offers_statuses,
        'taked_offers_statuses_dict': taked_offers_statuses_dict,
        'offers_with_takers_pending': offers_with_takers_pending,
        'offers_with_takers_accepted': offers_with_takers_accepted,
        'offers_with_takers_cancelled': offers_with_takers_cancelled,
    }
    
    return render(request, 'base/my_offers.html', context)

def take_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    offer.status = 'pending'

    relation = Take_offer(offer=offer, taker=request.user)
    offer.save()
    relation.save()

    messages.success(request, 'Zgłoszenie zostało wysłane. Oczekuj na zatwierdzenie przez autora oferty.')
    return redirect('offer_page', pk=pk)

def update_offer_status(request, pk, status):
    offer = Offer.objects.get(pk=pk)
    previous_status = offer.status
    offer.status = status
    offer.save()

    my_offers(request, status)
    return redirect('my_offers_page', status=previous_status)

def update_taking_offer_status(request, pk, taker, status):
    offer = Offer.objects.get(pk=pk)
    relation = Take_offer.objects.get(offer=offer, taker=taker)

    relation.status = status
    relation.save()
    
    previous_status = offer.status
    my_offers(request, status)
    return redirect('my_offers_page', status=previous_status)

def accept_offer(request, pk, taker):
    update_taking_offer_status(request, pk, taker, 'accepted')
    return update_offer_status(request, pk, 'in_progress')

def reject_offer(request, pk, taker):
    update_taking_offer_status(request, pk, taker, 'rejected')
    return update_offer_status(request, pk, 'waiting')

def cancel_offer(request, pk, taker):
    return update_taking_offer_status(request, pk=pk, taker=taker, status='cancelled')    
    # return update_offer_status(request, pk, 'cancelled')

def finish_offer(request, pk, taker):
    update_taking_offer_status(request, pk, taker=taker, status='finished')
    return update_offer_status(request, pk, 'finished')
