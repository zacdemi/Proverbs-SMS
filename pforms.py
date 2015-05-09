from proverbs import distincttag
from wtforms import validators, StringField, IntegerField, SelectField, SelectMultipleField, widgets
from flask_wtf import Form

tagtuple = distincttag()
frequency_list = [(7,"Daily"),(6,"6x Week"),(5,"5x Week"),(4,"4x Week"),(3,"3x Week"),(2,"2x Week"),(1,"1x Week")]

class searchtag(Form):
    search = StringField('Search Tag',[validators.DataRequired()],default="Work")

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class Subscribe(Form):
    phone = IntegerField('Telephone',[validators.DataRequired()])
    carrier = SelectField('Carrier',choices=[("AT&T","AT&T"),("Verizon","Verizon"),("Sprint","Sprint")])
    frequency = SelectField('Frequency',choices=frequency_list)
    taglist = MultiCheckboxField('Select Tags',choices=tagtuple,validators=[validators.Required()])

class Phone(Form):
    phone = IntegerField('Telephone',[validators.DataRequired()])

class UpdateSubscription(Form):
    taglist = MultiCheckboxField('Select Tags',choices=tagtuple,validators=[validators.Required()])
    frequency = SelectField('Frequency',choices=frequency_list)

class ConfirmCode(Form):
    phone = IntegerField('Telephone',[validators.DataRequired()])
    confirm_code = IntegerField('Enter Confirmation Code',validators=[validators.Required()])


