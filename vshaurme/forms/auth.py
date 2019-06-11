from flask import current_app, g
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, NoneOf
from flask_babel import lazy_gettext as _l

from vshaurme.models import User
from vshaurme.utils import load_badwords

from vshaurme.password_utils import has_numeric_and_alpha, has_upper_and_lower_letters

from vshaurme.yandex_metrika import YM_TARGET_REGISTRATION_DICT


def bad_words_check(form, field):
    data = load_badwords()
    for word in data:
        if field.data.find(word) >= 0:
            raise ValidationError(_l('The username should not contain any obscene words.'))


def has_has_numeric_and_alpha_check(form, field):
    if not has_numeric_and_alpha(field.data):
        raise ValidationError(_l('The password should contain both letters and digits.'))


def has_upper_and_lower_letters_check(form, field):
    if not has_upper_and_lower_letters(field.data):
        raise ValidationError(_l('The password should contain letters in different registers.'))


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Log in'))


class RegisterForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(1, 30)])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField(_l('Username'),
                           validators=[
                               DataRequired(),
                               Length(1, 20),
                               Regexp(
                                   '^[a-zA-Z0-9]*$',
                                   message=_l('The username should contain only a-z, A-Z and 0-9.')),
                               bad_words_check
                           ])
    password = PasswordField(_l('Password'),
                             validators=[
                                 DataRequired(),
                                 Length(10, 128),
                                 has_has_numeric_and_alpha_check,
                                 has_upper_and_lower_letters_check,
                                 EqualTo('password2'),
                             ])
    password2 = PasswordField(_l('Confirm password'), validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(_l('Submit'),
                         render_kw={
                             "onclick": "ym({}, 'reachGoal', {}); return true;".format(
                                 YM_TARGET_REGISTRATION_DICT['counter'],
                                 YM_TARGET_REGISTRATION_DICT['target_name']
                             )})

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_l('The email is already in use.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_l('The username is already in use.'))


class ForgetPasswordForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField(_l('Submit'))


class ResetPasswordForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField(_l('Password'), validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField(_l('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
