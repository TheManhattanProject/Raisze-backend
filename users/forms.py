from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        models=get_user_model()
        fields=('email','first_name', 'last_name','gender','date_of_birth','is_superuser')
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models=get_user_model()
        fields=('first_name', 'last_name','gender','date_of_birth','is_superuser')