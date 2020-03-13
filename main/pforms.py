import json
import phonenumbers

from main.proverbs import distincttag
from wtforms import (
    validators, StringField,TextField, IntegerField, SelectField, 
    SelectMultipleField, widgets, Form, ValidationError, SubmitField )
from flask_wtf import FlaskForm

tagtuple = distincttag()
frequency_list = [("7","Daily"),("6","6x Week"),("5","5x Week"),("4","4x Week"),("3","3x Week"),("2","2x Week"),("1","1x Week")]

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SignUp(FlaskForm):
    phone = StringField('Telephone',[validators.DataRequired()])
    submit = SubmitField('Submit') 

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        
class UserPreferences(FlaskForm):
    frequency = SelectField('Frequency',choices=frequency_list)
    taglist = MultiCheckboxField('Tags',choices=tagtuple,validators=[validators.Required()])

class ConfirmCode(FlaskForm):
    confirm_code = IntegerField('Enter Confirmation Code',validators=[validators.Required()])
