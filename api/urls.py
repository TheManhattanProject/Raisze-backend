from .views import *
from django.urls import path, include
from articles.views import *




urlpatterns = [
    # path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('create_article/', CreatePostView.as_view(), name='create_article'),
    path('articles/', ListArticleView.as_view(), name='articles'),
]
