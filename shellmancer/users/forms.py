from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from shellmancer.models import UserAccount

email_name = "E-mail"
password_name = "Password"
password_confirm_name = "Confirm Password"
user_name_name = "User Alias"


class UserSettingsForm(FlaskForm):
    user_name = StringField(user_name_name,
                            validators=[Length(max=120),
                                        Optional()],
                            render_kw={'placeholder': user_name_name})
    email = StringField(email_name,
                        validators=[DataRequired(),
                                    Length(min=4, max=32),
                                    Email()],
                        render_kw={"placeholder": email_name})
    image_file = FileField('Profile Pic', validators=[FileAllowed(['jpg', 'png'])])
    is_over_18 = BooleanField("Agree to Content that is 18+?")
    is_email_public = BooleanField("Share your email")

    submit = SubmitField('Update')

    @staticmethod
    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = UserAccount.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError(f'Alias "{user_name.data}" already belongs to a user')

    @staticmethod
    def validate_email(self, email):
        if email.data != current_user.email:
            user = UserAccount.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'Account already registered with {email.data}')

