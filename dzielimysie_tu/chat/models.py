from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Model reprezentujący pojedynczą wiadomość na czacie.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(verbose_name="Treść wiadomości")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Data i czas wysłania")

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"

    def __str__(self):
        return f"Wiadomość od {self.author.username} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
