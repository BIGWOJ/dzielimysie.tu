from django.urls import path
from . import views

# W konwencji dawajmy _page na końcu widoku w name

urlpatterns = [
    path('', views.home, name='home_page'),
    # path('offer/', views.offer, name='offer_page'),
]