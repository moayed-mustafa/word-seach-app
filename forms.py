



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, InputRequired, Optional,EqualTo


class SignupForm(FlaskForm):
    """ user signup form """
    gender_choices = [('male', 'male'),('female', 'female')]


    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),
                        Email(message="Enter a valid Email")]),
    image = StringField('(Optional) Image')
    gender = SelectField('Gender', choices=gender_choices)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
