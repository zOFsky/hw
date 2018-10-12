from django.core.mail import EmailMultiAlternatives
import os
from django.conf import settings

class EmailSender:

    def send_email(self, email, mail_subject, text_email, html_email, context):

        if "FRONTEND_HOST" in os.environ:
            context['host'] = os.environ['FRONTEND_HOST']

        context['domen'] = settings.DOMEN

        html_content = html_email.render(context)
        text_content = text_email.render(context)
        email = EmailMultiAlternatives(
            mail_subject, text_content, to=[email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
