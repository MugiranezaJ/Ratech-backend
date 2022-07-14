from django.urls import path

from .views import LoginView, Register, ResetPasswordView, SendOtpView

urlpatterns = [
    path('register', Register.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('reset_password', ResetPasswordView.as_view(), name="reset_password"),
    path('send_otp', SendOtpView.as_view(), name="sned_otp")
]