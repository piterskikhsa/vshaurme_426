from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email
from flask_babel import lazy_gettext as _l

from vshaurme.forms.user import EditProfileForm
from vshaurme.models import User, Role


class EditProfileAdminForm(EditProfileForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 254), Email()])
    role = SelectField(_l('Role'), coerce=int)
    active = BooleanField(_l('Active'))
    confirmed = BooleanField(_l('Confirmed'))
    submit = SubmitField(_l('Submit'))

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError(_l('The username is already in use.'))

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_l('The email is already in use.'))
