from django.core.mail import EmailMultiAlternatives
from .tokens import TokenGenerator

class EmailSender:

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

class EmailChangeSender:
    context = {}
    def __init__(self, user):
        self.user = user
    def generate_token(self, user, email):
        token_generator = TokenGenerator()
        context = {
            'uid': self.user.id,
            'token': token_generator.make_token(self.user),
            'new_email': email
        }
        self.context = context
        return context

    def send_email(self, mail_subject, text_email, html_email):
        html_content = html_email.render(self.context)
        text_content = text_email.render(self.context)
        to_email = self.context["new_email"]
        email = EmailMultiAlternatives(
            mail_subject, text_content, to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()