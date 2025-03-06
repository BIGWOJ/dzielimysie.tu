from django.urls import path
from . import views

# By convention, add _page at the end of the view in name
# Without _page because it's a function, not a view

urlpatterns = [
    path('not_done/', views.not_done, name='not_done_yet_page'),

    path('', views.home, name='home_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout_page'),
    path('register/', views.register_page, name='register_page'),

    path('create_offer/', views.create_offer, name='create_offer_page'),
    path('edit_offer/<str:pk>', views.edit_offer, name='edit_offer_page'),
    path('delete_offer/<str:pk>', views.delete_offer, name='delete_offer_page'),

    path('take_offer/<str:pk>', views.take_offer, name='take_offer'),  
    path('cancel_offer/<str:pk>', views.cancel_offer, name='cancel_offer'),  
    
    path('offer/<str:pk>', views.offer, name='offer_page'),
    path('offers/<str:offers_layout>', views.offers, name='offers_page'),
    path('category/<str:pk>', views.category, name='category_page'),
    
    path('follow_offer/<str:pk>', views.follow_offer, name='follow_offer'),
    path('follow_user/<str:pk>', views.follow_user, name='follow_user'),
    path('following/<str:page>', views.following, name='following_page'),

    path('profile/<str:pk>', views.user_profile, name='user_profile_page'),
    path('profile/<str:pk>/offers', views.user_offers, name='user_offers_page'),
    path('my_offers/<str:status>', views.my_offers, name='my_offers_page'),

    path('settings/', views.user_settings, name='user_settings_page'),
    path('chat/<str:pk>', views.chat, name='chat_page'),
]