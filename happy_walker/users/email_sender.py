from django.core.mail import EmailMultiAlternatives

class EmailSender:

    def send_email(self, email, mail_subject, text_email, html_email, context):

        html_content = html_email.render(context)
        text_content = text_email.render(context)
        email = EmailMultiAlternatives(
            mail_subject, text_content, to=[email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
