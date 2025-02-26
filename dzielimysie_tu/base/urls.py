from django.urls import path
from . import views

# W konwencji dawajmy _page na końcu widoku w name

urlpatterns = [
    path('', views.home, name='home_page'),
    path('offer/<str:pk>', views.offer, name='offer_page'),
    path('category/<str:pk>', views.category, name='category_page'),
    path('profile/<str:pk>', views.user_profile, name='user_profile_page'),
]