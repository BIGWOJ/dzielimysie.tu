from django.urls import path, include
from django.contrib import admin
from . import views
from chat import views as chat_views

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

    path('cancel_offer/<str:pk>', views.cancel_offer, name='cancel_offer'),
    path('finish_offer/<str:pk>', views.finish_offer, name='finish_offer'),
    path('republish_offer/<str:pk>', views.republish_offer, name='republish_offer'),

    path('take_offer/<str:pk>', views.take_offer, name='take_offer'),  
    path('accept_take_offer/<str:pk>/<str:taker>/', views.accept_take_offer, name='accept_take_offer'),
    path('reject_take_offer/<str:pk>/<str:taker>/', views.reject_take_offer, name='reject_take_offer'),  
    path('cancel_take_offer/<str:pk>/<str:taker>/<str:redirect_take_offers>/', views.cancel_take_offer, name='cancel_take_offer'),  
    path('finish_take_offer/<str:pk>/<str:taker>', views.finish_take_offer, name='finish_take_offer'),  
    path('finish_take_offer_finish_offer/<str:pk>/<str:taker>', views.finish_take_offer_finish_offer, name='finish_take_offer_finish_offer'),  
    
    path('offer/<str:pk>', views.offer, name='offer_page'),
    path('offers/<str:offers_layout>', views.offers, name='offers_page'),
    path('category/<str:pk>', views.category, name='category_page'),
    
    path('follow_offer/<str:pk>', views.follow_offer, name='follow_offer'),
    path('follow_user/<str:pk>', views.follow_user, name='follow_user'),
    path('following/<str:page>', views.following, name='following_page'),

    path('profile/<str:pk>', views.user_profile, name='user_profile_page'),
    path('add_opinion/<str:rated_user>/<str:take_offer>/<str:redirect_page>/', views.add_opinion, name='add_opinion_page'), 

    path('profile/<str:pk>/offers', views.user_offers, name='user_offers_page'),
    path('my_offers/<str:offers_status>/<str:take_offer_status>/', views.my_offers, name='my_offers_page'),
    path('my_take_offers/<str:status>', views.my_take_offers, name='my_take_offers_page'),

    path('settings/', views.user_settings, name='user_settings_page'),

    # path('chat/<str:pk>', views.chat, name='chat_page'),
    path('chat/', include('chat.urls')),
    path('send_message/<int:offer_id>/', views.send_message, name='send_message'),
    path('create_chat/<int:offer_id>/', views.create_chat, name='create_chat'),
    # path('offer/<int:pk>/', views.offer_detail, name='offer_page'),
    path('profile/<int:pk>/chats/', views.user_chats, name='user_chats'),
    path('<int:chat_id>/', chat_views.chat_view, name='chat'),
]