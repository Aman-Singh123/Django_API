from account.views import UserRegistrationView,UserLoginview,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView
from django.urls import path,include
urlpatterns=[
    path('registration/',UserRegistrationView.as_view(),name='Register'),
    path('login/',UserLoginview.as_view(),name='login'),
    path('check_profile',UserProfileView.as_view(),name='check_profile'),
    path('change_password',UserChangePasswordView.as_view(),name='change_password'),
    path('password_reset',SendPasswordResetEmailView.as_view(),name='mail_send'),
    path('reset-password/<uid>/<token>',UserPasswordResetView.as_view(),name='mail_send'),
]
