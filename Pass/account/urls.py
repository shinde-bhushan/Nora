from django.urls import path
from . import views
from . import views_new

urlpatterns = [
    path('home/', views.home, name='home'),
    # path('verifyotp/', views_new.UserSignupView.verify_mfa_setup_challenge, name='otp'),
    path('signup/', views_new.UserSignupView.as_view(), name='user_signup'),
    path('update/', views_new.UserSignupView.as_view(), name='user_update'),
    path('login/', views_new.UserLoginView.as_view(), name='login'),

]