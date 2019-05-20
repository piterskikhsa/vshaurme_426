from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from flask_babel import _

from vshaurme.extensions import mail


def send_mail(to, subject, template, **kwargs):
    # TODO: implement
    pass


def send_confirm_email(user, token, to=None):
    send_mail(subject=_('Email Confirm'), to=to or user.email, template='emails/confirm', user=user, token=token)


def send_reset_password_email(user, token):
    send_mail(subject=_('Password Reset'), to=user.email, template='emails/reset_password', user=user, token=token)


def send_change_email_email(user, token, to=None):
    send_mail(subject=_('Change Email Confirm'), to=to or user.email, template='emails/change_email', user=user, token=token)
