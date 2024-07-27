from django.urls import path,include
from accounts.views import UserSignUpView, UserLoginView,UserLogoutView,UserAccountUpdateView
urlpatterns = [
    path("signup/",UserSignUpView.as_view(),name='signup'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('profile/',UserAccountUpdateView.as_view(),name='profile'),
]