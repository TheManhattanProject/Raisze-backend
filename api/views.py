# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model

# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter

    
# class GoogleLogin(GoogleOAuth2Adapter):
#     adapter_class = GoogleOAuth2Adapter()
#     serializer_class = GoogleOAuth2Adapter.get_provider().get_serializer_class()
#     def get_callback_url(self, request):
#     # def get_callback_url(self, request)

#     def login(self, request, *args, **kwargs):
#         print(request)
#         # user,_ = get_user_model().objects.get_or_create(email=request.data['email'])
#         # print(user)
#         return super(GoogleLogin, self).login(request, *args, **kwargs)

from google.oauth2 import id_token
from google.auth.transport import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class GoogleLogin(PublicApiMixin, ApiErrorsMixin, APIView):
    




    
    
  


