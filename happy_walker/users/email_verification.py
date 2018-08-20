from django.core.mail import EmailMultiAlternatives
from .tokens import account_activation_token

class EmailVerification:

    def send_email(self, user, mail_subject, text_email, html_email):

        context = {
            'uid': user.id,
            'token': account_activation_token.make_token(user),
        }
        html_content = html_email.render(context)
        text_content = text_email.render(context)
        to_email = user.email
        email = EmailMultiAlternatives(
            mail_subject, text_content, to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
