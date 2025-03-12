from django.shortcuts import render, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required

@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    context = {
        'chat': chat,
        'messages': messages,
        'user_id': request.user.id #for javascript
    }
    return render(request, 'chat/chat.html',context)
    

