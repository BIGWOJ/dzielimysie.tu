from django.db import models
from django.urls import reverse
from django.conf import settings


class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    offer = models.ForeignKey('base.Offer', on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.offer.title} between {', '.join([str(p) for p in self.participants.all()])}"

    def get_chat_url(self):
        return reverse('chat:chat', kwargs={'chat_id': self.id})


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)  # for attachments

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} in {self.chat}: {self.text[:20]}"


class OfferApplication(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='application')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.applicant} applied to {self.chat.offer}"
