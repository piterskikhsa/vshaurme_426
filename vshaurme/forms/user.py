from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp
from flask_babel import lazy_gettext as _l

from vshaurme.models import User


class EditProfileForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(1, 30)])
    username = StringField(_l('Username'), validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='The username should contain only a-z, A-Z and 0-9.')])
    website = StringField(_l('Website'), validators=[Optional(), Length(0, 255)])
    location = StringField(_l('City'), validators=[Optional(), Length(0, 50)])
    bio = TextAreaField(_l('Bio'), validators=[Optional(), Length(0, 120)])
    submit = SubmitField(_l('Submit'))

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')


class UploadAvatarForm(FlaskForm):
    image = FileField(_l('Upload'), validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], _l('The file format should be .jpg or .png.'))
    ])
    submit = SubmitField(_l('Submit'))


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField(_l('Crop and Update'))


class ChangeEmailForm(FlaskForm):
    email = StringField(_l('New Email'), validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField(_l('Submit'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_l('The email is already in use.'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_l('Old Password'), validators=[DataRequired()])
    password = PasswordField(_l('New Password'), validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField(_l('Confirm Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField(_l('New comment'))
    receive_follow_notification = BooleanField(_l('New follower'))
    receive_collect_notification = BooleanField(_l('New collector'))
    submit = SubmitField(_l('Submit'))


class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField(_l('Public my collection'))
    submit = SubmitField(_l('Submit'))


class DeleteAccountForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField(_l('Submit'))

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError(_l('Wrong username.'))
