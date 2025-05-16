from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:chat_id>/', views.chat_view, name='chat'),
]