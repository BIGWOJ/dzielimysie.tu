from django.shortcuts import render, get_object_or_404
from .models import Chat
from django.contrib.auth.decorators import login_required

@login_required
def chat_view(request, chat_id):
    current_chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    user_chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    

    other_participant = current_chat.participants.exclude(id=request.user.id).first()

    return render(request, 'chat/chat.html', {
        'current_chat': current_chat,
        'user_chats': user_chats,
        'other_participant': other_participant,  
    })


