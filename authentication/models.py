from django.core.mail import EmailMultiAlternatives

# Create your models here.
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.translation import gettext as _
from smtplib import SMTPException
import logging


logger = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}{}".format(
            instance.request.build_absolute_uri(),
            reset_password_token.key),
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title=_("GPS Tracking Application")),
        # message:
        email_plaintext_message,
        # from:
        _("GPS Tracking Supporter"),
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    try:
        msg.send()
    except SMTPException as e:
        logger.error('There was an error sending an email: {}'.format(e))
