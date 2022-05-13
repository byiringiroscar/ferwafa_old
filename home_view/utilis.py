from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data, attach):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.attach(attach.name, attach.read(), attach.content_type)
        email.send()

