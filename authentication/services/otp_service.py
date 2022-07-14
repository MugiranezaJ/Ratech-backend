from authentication.models import Otp
from random import randint
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

class OtpService:
    def generate(self, kwargs):
        email = kwargs.get('email')
        code = str(randint(100000, 999999))

        otp = Otp(email=email, code=code)

        otp.save()
        return code

    def verify(self, username, code):
        otp_query = Otp.objects.filter(email=username, code=code, is_verified=False)
        if not otp_query.exists():
            return False

        otp = otp_query.first()
        if otp:
            otp.is_verified = True
            otp.save()

        return otp is not None

    def verify_with_phone_email(email, phone, code):
        email_otp = Otp.objects.filter(email=email, code=code, is_verified=False)
        otp = email_otp.first()

        if not otp:
            return False

        otp.is_verified = True
        otp.save()

        return True

    def verified(self, email, phone):
        return Otp.objects.filter(email=email, phone=phone, is_verified=True).exists()

    def mark_delivered(self, code, to):
        try:
            otp_query = Otp.objects.get(email=to, code=code)

            otp_query.is_delivered = True
            otp_query.save()
        except BaseException as e:
            print("failed to mark otp as delivered")
    
    def send_email(self, recipient, message):
        template = render_to_string("email_template.html", {"message": message})
        res = dict()
        try:
            send_mail(
                'Password reset',
                template,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False
            )
            # self.mark_delivered(self, message, recipient)
            res["message"] = "Otp email sent successfully!"
            return res
        except Exception as e:
            raise e