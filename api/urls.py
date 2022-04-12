from .views import *
from django.urls import path, include
from articles.views import *
from userstatistics.views import *




urlpatterns = [
    # path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('create_article/', CreatePostView.as_view(), name='create_article'),
    path('articles/', ListArticleView.as_view(), name='articles'),
    path('create_financial_sheets/', CreateFinancialSheetsView.as_view(), name='create-financial-sheets'),
    path('save_campaigns/', CreateSaveCampaignsView.as_view(), name='save-campaigns'),
]
