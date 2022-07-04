from .views import *
from django.urls import path, include
from articles.views import *
from userstatistics.views import *
from users.views import *
from tools.views import *
from campaign_statistics.views import *



urlpatterns = [
    # path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('create_article/', CreatePostView.as_view(), name='create_article'),
    path('articles/', ListArticleView.as_view(), name='articles'),
    path('create_financial_sheets/', CreateFinancialSheetsView.as_view(), name='create-financial-sheets'),
    path('save_campaigns/', CreateSaveCampaignsView.as_view(), name='save-campaigns'),
    path('complete_registration', UpdateUser.as_view(), name='update-user'),
    path('valuation/', CreateValuationView.as_view(), name='valuation'),
    path('tools/create_tools', CreateToolsView.as_view(), name='create-tools'),
    path('tools/update_tools', UpdateToolsView.as_view(), name='update-tools'),
    path('tools/list_tools', ListToolsView.as_view(), name='list-tools'),
    path('campaign/popular', PopularCampaignsView.as_view(), name="popular-campaign"),
    path('campaign/list', CampaignListAPIView.as_view(), name="campaign-list"),
    path('campaign/subcategory', SubPopularCampaignsView.as_view(), name="subpopular-campaigns"),
    path('campaign/update/<str:id>', UpdateCampaignAPIView.as_view(), name="update-campaigns"),
    path('campaign_image/list', ListCreateCampaignImageAPIView.as_view(),name="list-campaign-image"),
]
