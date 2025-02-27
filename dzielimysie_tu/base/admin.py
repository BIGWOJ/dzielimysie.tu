from django.contrib import admin
from .models import *
# Register your models here.

# After creating the models, we need to register them in the admin panel.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Offer)
admin.site.register(Message)
