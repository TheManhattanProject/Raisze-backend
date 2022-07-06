from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/rest-auth/google/'
    client_class = OAuth2Client
    # def post(self, request, *args, **kwargs):
    #     response = super(GoogleLogin, self).post(request, *args, **kwargs)
    #     print(response.data.get('key'))
    #     token = Token.objects.get(key=response.data.get('key'))
    #     print("adadadadadadadadad")
    #     print(token.user)

        # return Response({'token':token.key})
    # adapter_class = GoogleOAuth2Adapter()
    # serializer_class = GoogleOAuth2Adapter.get_provider().get_serializer_class()
    # def get_callback_url(self, request):
    # # def get_callback_url(seclf, request)

    # def login(self, request, *args, **kwargs):
    #     print(request)
    #     # user,_ = get_user_model().objects.get_or_create(email=request.data['email'])
    #     # print(user)
    #     return super(GoogleLogin, self).login(request, *args, **kwargs)

# from google.oauth2 import id_token
# from google.auth.transport import requests

# from allauth.socialaccount.providers.oauth2.views import (
#     OAuth2Adapter,
#     OAuth2CallbackView,
#     OAuth2LoginView,
# )
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


# class GoogleLogin(PublicApiMixin, ApiErrorsMixin, APIView):
    




    
    
  


