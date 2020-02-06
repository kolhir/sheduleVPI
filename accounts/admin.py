from django.contrib import admin
from .models import BotUser, User_profile
# Register your models here.

@admin.register(User_profile)
class User_profileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tt_json', 'group']

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_name', 'name', 'last_name', 'group']


