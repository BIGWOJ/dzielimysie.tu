from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm


# Create your views here.
def chat_room(request):
    messages = Message.objects.order_by('-timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()
            return redirect('chat_room')
    else:
        form = MessageForm()
    return render(request, 'chat/chat_room.html', {'messages': messages, 'form': form})