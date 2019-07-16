from django.contrib import admin
from .models import Mail, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Mail)
admin.site.register(User, UserAdmin)
