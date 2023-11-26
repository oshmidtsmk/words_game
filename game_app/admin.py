# game_app/admin.py

from django.contrib import admin
from django.contrib.auth.models import Group, User
from . import models
# Register your models here.


admin.site.register(models.Word)


admin.site.register(models.Profile)

#Unregister Groups
# admin.site.unregister(Group)
#
# #Mix profile into user info
# class ProfileInline(admin.StackedInline):
#     model = models.Profile
#
# #Extend user model
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     #Displaying user name fields on admin page
#     fields = ["username"]
#     inlines = [ProfileInline]
#
# #Unregister initial user
# admin.site.unregister(User)
#
# #register user and Profile
# admin.site.register(User, UserAdmin)
