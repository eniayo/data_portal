from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import DataRequired
class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class RegisterForm(Form):
    name = StringField("Ad", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This FIeld")]) 
    username = StringField("Userrname", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do not Match")
    ])

    confirm = PasswordField("confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])
