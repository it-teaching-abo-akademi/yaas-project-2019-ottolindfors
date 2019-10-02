from django.urls import path, re_path
from . import views, rest_views


# These are the (sub) urls after /auction/ url
app_name = 'auction'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('create/', views.CreateAuction.as_view(), name='create'),
    path('edit/<int:id>/', views.EditAuction.as_view(), name='edit'),
    # ^ mathes the beginning of a string, \d matches any digit, + matches one or more
    # re_path(r'^edit/(\d+)/$', views.EditAuction.as_view(), name='edit'),    # url -> edit/digits
    re_path(r'^bid/(\d+)/$', views.bid, name='bid'),
    re_path(r'^ban/(\d+)$', views.ban, name='ban'),
    path('resolve/', views.resolve, name='resolve'),
]
