from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length,InputRequired,ValidationError,EqualTo
import re
from pokemon.models.models import USER1

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    abilities = StringField("Abilities", validators=[DataRequired()])
    submit = SubmitField('Submit')
    
     
class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("email",validators=[DataRequired()],render_kw={"class": "border-2 -gray-300 rounded-lg p-2 w-80","placeholder": "email",},)
    password = PasswordField("Password", validators=[InputRequired(),Length(min=6),])
    cpassword = PasswordField("Confirm Password",  validators=[InputRequired(),EqualTo("password", message="passwords must match"),Length(min=6),],)
    submit = SubmitField("Register")
    
    def validate_name(self,name):
        if len(name.data) < 3:
            raise ValidationError("Username must be at least 3 characters long")

        user = USER1.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

        if not re.match(email_pattern, email.data):
            raise ValidationError("Invalid email")

        mail = USER1.query.filter_by(email=email.data).first()

        if mail:
            raise ValidationError("Email is already taken")
        

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
    
    