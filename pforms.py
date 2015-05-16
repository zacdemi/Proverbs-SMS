from proverbs import distincttag
from wtforms import validators, StringField,TextField, IntegerField, SelectField, SelectMultipleField, widgets
from flask_wtf import Form

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

class Phone(Form):
    phone = TextField('Telephone',[validators.DataRequired(),validators.Length(min=10, max=10)])
   
class UserPreferences(Form):
    frequency = SelectField('Frequency',choices=frequency_list)
    taglist = MultiCheckboxField('Select Tags',choices=tagtuple,validators=[validators.Required()])

class ConfirmCode(Form):
    confirm_code = IntegerField('Enter Confirmation Code',validators=[validators.Required()])


