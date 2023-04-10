from django.urls import path
from .views import Home,SignUpView,account_verify,SignInView,logout_view

urlpatterns = [
    path('',Home.as_view(),name = 'home'),
    path('sign-up/',SignUpView.as_view(),name = "sign-up"),
    path('account-verify/<slug:token>',account_verify,name="account-verify"),
    path('sign-in/',SignInView.as_view(), name = "sign-in"),
    path('sign-out/',logout_view, name = "sign-out")

]
