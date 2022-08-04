from django.urls import path

from .views import LoginView, Register, ResetPasswordView, SendOtpView, ChangePasswordView

urlpatterns = [
    path('register', Register.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('reset_password', ResetPasswordView.as_view(), name="reset_password"),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('send_otp', SendOtpView.as_view(), name="send_otp")
]