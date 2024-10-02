from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.urls import reverse


class EmailSender:
    def __init__(self, user, request):
        self.user = user
        self.request = request

    def send_verification_email(self):
        token = RefreshToken.for_user(self.user).access_token
        verify_url = reverse('verify-email')
        absurl = self.request.build_absolute_uri(f'{verify_url}?token={str(token)}')
        email_body = f'Hi {self.user.first_name},\n\nUse the link below to verify your email:\n{absurl}'
        
        # Send verification email
        send_mail(
            subject='Verify your email',
            message=email_body,
            from_email='your-email@example.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )
