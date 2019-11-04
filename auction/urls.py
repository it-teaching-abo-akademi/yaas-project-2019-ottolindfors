from django.urls import path, re_path
from . import views, rest_views


# These are the (sub) urls after /auction/ url
app_name = 'auction'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('create/', views.CreateAuction.as_view(), name='create'),
    path('edit/<int:id>/', views.EditAuction.as_view(), name='edit'),
    path('edit/no-signin/<str:token>/', views.EditAuctionNoSignIn.as_view(), name='edit-no-signin'),
    path('bid/<int:item_id>/', views.Bid.as_view(), name='bid'),  # /auction/bid/{id} : re_path(r'^bid/(\d+)/$', views.bid, name='bid')
    re_path(r'^ban/(\d+)$', views.ban, name='ban'),
    path('resolve/', views.resolve, name='resolve'),
    path('confirm/', views.ConfirmAuction.as_view(), name='confirm'),
    path('banned/', views.banned_auctions, name='banned-auctions')
]
