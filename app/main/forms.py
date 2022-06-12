from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, TelField, FieldList, FormField, EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = TelField('Phone Number', validators=[DataRequired()])
    contact_email = EmailField('Contact Email', validators=[DataRequired()])
    submit = SubmitField('Save')


class ContactForm(FlaskForm):
    chain = SelectField(u'Blockchain', choices=[('Kusama', 'Kusama'), ('Polkadot', 'Polkadot')], validators=[DataRequired()])
    