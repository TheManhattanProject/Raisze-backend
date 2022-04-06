import imp
import os
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from urllib.parse import urlsplit
from django.utils.encoding import escape_uri_path, iri_to_uri
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from userstatistics.models import UserInfo
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import import_callable
from dj_rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer


if 'allauth' in settings.INSTALLED_APPS:
    from allauth.account import app_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.forms import \
        ResetPasswordForm as DefaultPasswordResetForm
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (filter_users_by_email,
                                       user_pk_to_url_str, user_username)



class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.CharField()
    date_of_birth = serializers.DateField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username=None

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
        'password1': self.validated_data.get('password1', ''),
        'password2': self.validated_data.get('password2', ''),
        'email': self.validated_data.get('email', ''),
        'first_name': self.validated_data.get('first_name', ''),
        'last_name': self.validated_data.get('last_name', ''),
        'date_of_birth': self.validated_data.get('date_of_birth', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.date_of_birth=self.data.get('date_of_birth')
        
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
            
        user.save()
        userd=request.data.get('userdetails')
        if userd:
            UserInfo(user=user,os=userd.get('os'),browser=userd.get('browser'),ip=userd.get('ip')).save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

class UserSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        model=get_user_model()
        fields = ('gender', 'first_name', 'last_name','date_of_birth','pk',)

    def update(self, instance, validated_data):
        # userprofile_serializer = self.fields['profile']
        # userprofile_instance = instance.userprofile
        # userprofile_data = validated_data.pop('userprofile', {})

        # # to access the 'company_name' field in here
        # # company_name = userprofile_data.get('company_name')

        # # update the userprofile fields
        # userprofile_serializer.update(userprofile_instance, userprofile_data)

        instance = super().update(instance, validated_data)
        return instance