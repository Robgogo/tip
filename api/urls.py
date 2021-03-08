from django.contrib import admin
from django.urls import path, include, re_path

from rest_auth.registration.views import VerifyEmailView, RegisterView
from api.views.product import ProductsViewSet, ProductDetailViewSet, CategoryViewSet, CategoryDetailViewSet,\
    BrandViewSet, BrandDetailViewSet, SpeciesViewSet, SpeciesDetailViewSet
from api.views.blog import BlogsViewSet, BlogDetailViewSet

urlpatterns = [
    # Admin paths
    path('admin/', include('rest_auth.urls')),
    path('admin/registration/', include('rest_auth.registration.urls')),
    re_path(r'^admin/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^admin/account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),

    # General paths

    # Protected paths
]
