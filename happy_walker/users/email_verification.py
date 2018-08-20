from django.core.mail import EmailMultiAlternatives
from .tokens import TokenGenerator

class EmailVerification:

    def send_email(self, user, mail_subject, text_email, html_email):

        token_generator = TokenGenerator()

        context = {
            'uid': user.id,
            'token': token_generator.make_token(user),
        }
        html_content = html_email.render(context)
        text_content = text_email.render(context)
        to_email = user.email
        email = EmailMultiAlternatives(
            mail_subject, text_content, to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
