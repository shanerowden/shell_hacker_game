from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, Optional
)
from shellmancer.models import UserAccount

email_name = "E-mail"
password_name = "Password"
password_confirm_name = "Confirm Password"

campaign_title = "Title of Campaign"
campaign_descrip = "Campaign Description"

user_name_name = "User Alias"

class RegisterForm(FlaskForm):
    email = StringField(email_name,
                        validators=[DataRequired(),
                                    Length(min=4, max=32),
                                    Email()],
                        render_kw={"placeholder": email_name})

    password = PasswordField(password_name,
                             validators=[DataRequired(),
                                         Length(min=8)],
                             render_kw={"placeholder": password_name})

    password_confirm = PasswordField(password_confirm_name,
                                     validators=[DataRequired(),
                                                 EqualTo('password')],
                                     render_kw={"placeholder": password_confirm_name})
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_email(self, email):
        user = UserAccount.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'Account already registered with {email.data}')


class LoginForm(FlaskForm):
    email = StringField(email_name,
                        validators=[DataRequired(),
                                    Length(min=4, max=32),
                                    Email()],
                        render_kw={"placeholder": email_name})

    password = PasswordField(password_name,
                             validators=[DataRequired(),
                                         Length(min=8)],
                             render_kw={"placeholder": password_name})

    remember = BooleanField("Remember?")

    submit = SubmitField('Login')


class NewCampaignForm(FlaskForm):
    title = StringField(campaign_title,
                        validators=[DataRequired()],
                        render_kw={'placeholder': campaign_title})
    descrip = TextAreaField(campaign_descrip,
                            validators=[DataRequired(),
                                        Length(min=50, max=250)],
                            render_kw={'placeholder': campaign_descrip})
    submit = SubmitField('Create')


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
    agree_over_18 = BooleanField("Agree to Content that is 18+?")

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

    # id = db.Column(db.Integer, primary_key=True)
    # user_name = db.Column(db.String(120), nullable=True)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default="static/default.jpg")
    # password = db.Column(db.String(60), nullable=False)
    # account_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # agree_over_18 = db.Column(db.Boolean, default=False)
    # is_admin = db.Column(db.Boolean, default=False)