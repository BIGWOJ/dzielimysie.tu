from django.urls import path
from . import views

# By convention, add _page at the end of the view in name

urlpatterns = [
    path('', views.home, name='home_page'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),

    path('offer/<str:pk>', views.offer, name='offer_page'),
    path('category/<str:pk>', views.category, name='category_page'),

    path('profile/<str:pk>', views.user_profile, name='user_profile_page'),
]