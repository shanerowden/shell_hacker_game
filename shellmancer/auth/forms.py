from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from shellmancer.models import UserAccount

email_name = "E-mail"
password_name = "Password"
password_confirm_name = "Confirm Password"


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



class RequestResetForm(FlaskForm):
    email = StringField(email_name,
                        validators=[DataRequired(),
                                    Length(min=4, max=32),
                                    Email()],
                        render_kw={"placeholder": email_name})

    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        user = UserAccount.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Register first.')


class PasswordResetForm(FlaskForm):
    password = PasswordField(password_name,
                             validators=[DataRequired(),
                                         Length(min=8)],
                             render_kw={"placeholder": password_name})

    password_confirm = PasswordField(password_confirm_name,
                                     validators=[DataRequired(),
                                                 EqualTo('password')],
                                     render_kw={"placeholder": password_confirm_name})
    submit = SubmitField('Reset Password')

class RequestVerifyForm(FlaskForm):
    submit = SubmitField('Send Verification Email')
