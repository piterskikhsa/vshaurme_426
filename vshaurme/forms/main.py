import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length
from flask_babel import lazy_gettext as _l


class DescriptionForm(FlaskForm):
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(0, 500)])
    submit = SubmitField(_l('Submit'))


class TagForm(FlaskForm):
    tag = StringField(_l('Add Tag (use space to separate)'), validators=[Optional(), Length(0, 64)])
    submit = SubmitField(_l('Submit'))


class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField(_l('Submit'),
                         render_kw={
                             "onclick": "ym({}, 'reachGoal', '{}'); return true;".format(
                                 os.getenv('YA_COUNTER'),
                                 os.getenv('YA_POSTING_COMMENT')
                             )})
