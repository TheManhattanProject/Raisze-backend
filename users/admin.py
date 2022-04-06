from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm,CustomUserCreationForm

CustomUser=get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    ordering = ('email',)
    add_fieldsets = (('information',{'fields':('email','password1', 'password2','first_name','last_name','date_of_birth',),},),('Advanced options',{'classes':('collapse',),'fields': ('is_superuser',)},),)
    fieldsets=(('information',{'fields':('email','first_name','last_name','gender','date_of_birth',),},),('Advanced options',{'classes':('collapse',),'fields': ('is_superuser',)},),)

    list_display=['email','first_name','last_name']
    search_fields = ('email',)



admin.site.register(CustomUser,CustomUserAdmin)