from .views import *
from django.urls import path, include
from articles.views import *
from userstatistics.views import *
from users.views import *
from tools.views import *
from campaign_statistics.views import *
from orders.views import *



urlpatterns = [
    # path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('create_article/', CreatePostView.as_view(), name='create_article'),
    path('articles/list/', ListArticleView.as_view(), name='articles'),
    path('articles/update/<str:id>/', UpdateArticlesView.as_view(), name='articles-update'),
    path('create_financial_sheets/', CreateFinancialSheetsView.as_view(), name='create-financial-sheets'),
    path('save_campaigns/', CreateSaveCampaignsView.as_view(), name='save-campaigns'),
    path('complete_registration', UpdateUser.as_view(), name='update-user'),
    path('valuation/', CreateValuationView.as_view(), name='valuation'),
    path('tools/update/<int:id>', UpdateToolsView.as_view(), name='update-tools'),
    path('transaction/update/<int:id>', UpdateTransactionAPIView.as_view(), name='update-transaction'),
    path('transaction/create/', PaymentAPIView.as_view(), name='create-transaction'),
    path('tools/create/', CreateToolsView.as_view(), name='create-tools'),
    path('shipping/create/', ListCreateShippingsAPIView.as_view(), name='create-ships'),
    path('callback/', CallbackAPIView.as_view(), name='callback-transaction'),
    path('payments/<int:id>', PaymentView.as_view(), name='payment-transaction'),
    path('tools/popular/', PopularToolsView.as_view(), name='popukar-tools'),
    path('tools/list', ListToolsView.as_view(), name='list-tools'),
    path('campaign/popular/', PopularCampaignsView.as_view(), name="popular-campaign"),
    path('campaign/unpaglist/', CampaignListUnPagAPIView.as_view(), name="campaign-list-unpaginated"),
    path('campaign/list/', ListCreateCampaignAPIView.as_view(), name="campaign-list-paginated"),
    path('campaign/user/', UserCampaignAPIView.as_view(), name="campaign-user-paginated"),
    path('campaign/subcategory/', SubPopularCampaignsView.as_view(), name="subpopular-campaigns"),
    path('campaign/update/<str:id>', UpdateCampaignAPIView.as_view(), name="update-campaigns"),
    path('campaign/add_comment/<str:id>', CreateCommentForCampaignAPIView.as_view(), name="comment-campaigns"),
    path('campaign_image/list/', ListCreateCampaignImageAPIView.as_view(),name="list-campaign-image"),
    path('category/list/', ListCreateCategoryAPIView.as_view()),
    path('unpagcategory/list/', ListCreateCategoryUnPagAPIView.as_view()),
    path('category/update/<str:id>', UpdateCategoryAPIView.as_view()),
    path('tool_category/list/', ListCreateToolCategoryAPIView.as_view()),
    path('tool_unpagcategory/list/', ListCreateToolCategoryUnPagAPIView.as_view()),
    path('tool_category/update/<str:id>', UpdateToolCategoryAPIView.as_view()),
    path('subcategory/list/', ListCreateSubCategoryAPIView.as_view()),
    path('unpagsubcategory/list/', ListCreateSubCategoryUnPagAPIView.as_view()),
    path('subcategory/update/<int:id>', UpdateSubCategoryAPIView.as_view()),
    path('comment/add_reply/<int:id>', CreateReplyForCampaignAPIView.as_view()),
    path('tags/list/', ListCreateTagsAPIView.as_view()),
    path('tags/update/<int:id>', UpdateTagsAPIView.as_view()),
    path('gender/list/', ListCreateGenderAPIView.as_view()),
    path('gender/update/<int:id>', UpdateGenderAPIView.as_view()),
    path('timeline/list/', ListCreateTimelineAPIView.as_view()),
    path('timeline/update/<int:id>', UpdateTimelineAPIView.as_view()),
    path('items/list/', ListCreateItemsAPIView.as_view()),
    path('items/update/<int:id>', UpdateItemsAPIView.as_view()),
    path('reward/list/', ListCreateRewardAPIView.as_view()),
    path('reward/update/<str:id>', UpdateRewardAPIView.as_view()),
    path('update/user/<int:id>/', UpdateUser.as_view()),
    path('user/transaction/', UserTransactionListAPIView.as_view()),
]
