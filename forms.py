from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Regexp

class ViolationForm(FlaskForm):
    vehicle_number = StringField('Vehicle Number', validators=[
        DataRequired(), 
        Regexp(r'^[A-Z0-9-]+$', message="Invalid vehicle number format")
    ])
    violation_type = SelectField('Violation Type', choices=[
        ('No Helmet', 'No Helmet'),
        ('Over Speeding', 'Over Speeding'),
        ('Red Light Jump', 'Red Light Jump'),
        ('No License', 'No License'),
        ('Wrong Parking', 'Wrong Parking')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    fine_amount = FloatField('Fine Amount (₹)', validators=[DataRequired()])
    submit = SubmitField('Log Violation')
    # ... existing ViolationForm ...

from wtforms import PasswordField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')