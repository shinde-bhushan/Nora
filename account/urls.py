from django.urls import path
from . import views
from . import views_new

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('verifyotp/', views.verify_signup_otp, name='otp'),
    path('signup/', views_new.UserSignupView.as_view(), name='user_signup'),
]