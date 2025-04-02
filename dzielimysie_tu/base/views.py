from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Offer, User, Photo, Take_offer, Opinion
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
    
    taked_statuses = ['waiting', 'accepted']

    # __in is used to filter by multiple values
    user_is_taker = Take_offer.objects.filter(offer=offer, taker=request.user, status__in=taked_statuses).exists()

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
    opinions_overall = user.opinions_overall
    latest_opinions = Opinion.objects.filter(rated_user=user).order_by('-date')[:3]

    context = {'user': user, 'latest_opinions': latest_opinions, 'opinions_overall': opinions_overall}
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
    offers = Offer.objects.filter(creator=pk, status__in=['waiting', 'pending', 'in_progress'])
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
        data = request.POST.copy()
        data['place'] = data.get('place', 'Szczecin')
        form = Offer_Form(data, request.FILES)

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

def my_offers(request, offers_status, take_offer_status="None"):
    offers = Offer.objects.filter(creator=request.user, status=offers_status)
    offers_statuses = Offer.statuses

    # __ is used to access field of the related model
    if take_offer_status != "None":
        offers_with_takers = [(offer, Take_offer.objects.filter(offer=offer, offer__creator=request.user, status=take_offer_status)) for offer in offers]

    else:
        offers_with_takers = [(offer, Take_offer.objects.filter(offer=offer, offer__creator=request.user)) for offer in offers]

    take_offers = [take_offer for _, take_offer_queryset in offers_with_takers for take_offer in take_offer_queryset]

    take_offers_without_opinions = [take_offer for take_offer in take_offers if not Opinion.objects.filter(offer=take_offer.offer, rated_user=take_offer.taker).exists()]

    context = {
        'offers': offers,
        'offers_status': offers_status,
        'offers_statuses': offers_statuses,
        'offers_with_takers': offers_with_takers,
        'take_offers_without_opinions': take_offers_without_opinions
    }
    
    return render(request, 'base/my_offers.html', context)

def my_take_offers(request, status):
    take_offers = Take_offer.objects.filter(taker=request.user, status=status)
    take_offers_statuses = Take_offer.statuses

    context = {
        'take_offers': take_offers, 
        'take_offers_status': status, 
        'take_offers_statuses': take_offers_statuses
    }
    return render(request, 'base/my_take_offers.html', context)

def take_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    offer.status = 'pending'

    try:
        relation = Take_offer.objects.get(offer=offer, taker=request.user)
        relation.status = 'waiting'
    except Take_offer.DoesNotExist:
        relation = Take_offer(offer=offer, taker=request.user)

    offer.save()
    relation.save()

    return redirect('offer_page', pk=pk)

def update_offer_status(request, pk, status, redirect_take_offers=False):
    offer = Offer.objects.get(pk=pk)
    previous_status = offer.status
    offer.status = status
    offer.save()

    if redirect_take_offers == "offer_page":
        return redirect('offer_page', pk=pk)
    elif redirect_take_offers == "True":
        return my_take_offers(request, status)
    else:
        return my_offers(request, offers_status=previous_status)

def get_takers_after(offer, taker, status):
    return Take_offer.objects.filter(offer=offer, status='waiting').exclude(taker=taker)

def update_take_offer_status(request, pk, taker, status, previous_offers_status, redirect_take_offers=False):
    offer = Offer.objects.get(pk=pk)
    relation = Take_offer.objects.get(offer=offer, taker=taker)
    previous_take_status = relation.status

    relation.status = status
    relation.save()

    if status == 'accepted':
        takers_after = get_takers_after(offer, taker, relation.status)
        if takers_after:
            for take_offer in takers_after:
                take_offer.status = 'rejected'
                take_offer.save()

    if redirect_take_offers == "offer_page":
        return redirect('offer_page', pk=pk)
    elif redirect_take_offers == "True":
        return my_take_offers(request, status=previous_take_status)
    else:
        return my_offers(request, offers_status=previous_offers_status, take_offer_status=previous_take_status)

def accept_take_offer(request, pk, taker):
    previous_offers_status = get_previous_offer_status(pk)

    update_take_offer_status(request, pk, taker, 'accepted', previous_offers_status=previous_offers_status)
    
    return update_offer_status(request, pk, 'in_progress')

def get_previous_offer_status(pk):
    return Offer.objects.get(pk=pk).status

def reject_take_offer(request, pk, taker):
    takers_after = get_takers_after(pk, taker, 'accepted')
    previous_offer_status = get_previous_offer_status(pk)

    if not takers_after:
        update_offer_status(request, pk, 'waiting')

    return update_take_offer_status(request, pk, taker, 'rejected', previous_offers_status=previous_offer_status)

def cancel_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    take_offers = Take_offer.objects.filter(offer=offer)
    
    if take_offers:
        for take_offer in take_offers:
            take_offer.status = 'cancelled'
            take_offer.save()

    offer = Offer.objects.get(pk=pk)
    offer.status = 'cancelled'
    offer.save()

    return redirect('offer_page', pk=pk)

def cancel_take_offer(request, pk, taker,redirect_take_offers=False):
    take_offer = Take_offer.objects.get(offer=pk, taker=taker)
    takers_after = get_takers_after(pk, taker, take_offer.status)
    previous_offers_status = get_previous_offer_status(pk)

    if not takers_after:
        update_offer_status(request, pk, 'waiting', redirect_take_offers=redirect_take_offers)

    return update_take_offer_status(request, pk=pk, taker=taker, redirect_take_offers=redirect_take_offers, status='cancelled', previous_offers_status=previous_offers_status)    

def finish_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    take_offers = Take_offer.objects.filter(offer=offer)
    
    if take_offers:
        for take_offer in take_offers:
            take_offer.status = 'cancelled'
            take_offer.save()

    offer = Offer.objects.get(pk=pk)
    offer.status = 'finished'
    offer.save()

    return redirect('offer_page', pk=pk)

def finish_take_offer_finish_offer(request, pk, taker):
    previous_offers_status = get_previous_offer_status(pk)
    finish_offer(request, pk=pk)

    return update_take_offer_status(request, pk, taker=taker, status='finished', previous_offers_status=previous_offers_status)

def finish_take_offer(request, pk, taker):
    previous_offers_status = get_previous_offer_status(pk)
    offer = Offer.objects.get(pk=pk)
    offer.status = 'waiting'
    offer.save()

    return update_take_offer_status(request, pk=pk, taker=taker, status='finished', previous_offers_status=previous_offers_status)

def republish_offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    offer.status = 'waiting'
    offer.save()

    return redirect('offer_page', pk=pk)

#Need to add redirect to chat
def add_opinion(request, rated_user, take_offer, redirect_page):
    rated_user = User.objects.get(pk=rated_user)
    take_offer_offer = Take_offer.objects.get(pk=take_offer).offer

    if redirect_page == 'my_take_offers':
        take_offer = Take_offer.objects.get(offer=take_offer_offer, taker=request.user)

    if redirect_page == 'my_offers':
        take_offer = Take_offer.objects.get(offer=take_offer_offer, taker=rated_user)
        
    opinion = Opinion.objects.filter(rated_user=rated_user, author=request.user, offer=take_offer.offer)
    opinion_exists = opinion.exists()

    if request.method == 'POST':
        opinion = Opinion(offer=take_offer.offer, rated_user=rated_user, author=request.user, text=request.POST['opinion_text'], rating=request.POST['rating'])
        opinion.save()

        rated_user.opinions_count += 1
        rated_user.opinions_sum += int(request.POST['rating'])
        rated_user.opinions_overall = rated_user.opinions_sum / rated_user.opinions_count
        rated_user.save()

        match redirect_page:
            case "my_take_offers":
                take_offer.taker_to_creator_opinion = True
                take_offer.save()
                return my_take_offers(request, status='finished')
            case "my_offers":
                take_offer.creator_to_taker_opinion = True
                take_offer.save()
                return my_offers(request, offers_status='finished', take_offer_status='finished')
            case "chat":
                #TO DO
                pass
    
    latest_opinions = Opinion.objects.filter(rated_user=rated_user).order_by('-date')[:3]

    context = {'rated_user': rated_user, 'take_offer': take_offer, 'latest_opinions': latest_opinions, 'opinion_exists': opinion_exists}
    return render(request, 'base/add_opinion.html', context=context)
