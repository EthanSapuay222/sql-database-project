from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

class SightingForm(FlaskForm):
    species_id = SelectField('Species', coerce=int, validators=[DataRequired()])
    location_id = SelectField('Location', coerce=int, validators=[DataRequired()])
    sighting_date = DateField('Sighting Date', validators=[DataRequired()])
    sighting_time = TimeField('Sighting Time', validators=[Optional()])
    number_observed = IntegerField('Number Observed', validators=[NumberRange(min=1)], default=1)
    observer_name = StringField('Observer Name', validators=[DataRequired()])
    observer_contact = StringField('Contact (Email or Phone)', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes', validators=[Optional()])

class EnvironmentalReportForm(FlaskForm):
    location_id = SelectField('Location', coerce=int, validators=[DataRequired()])
    report_type = SelectField('Report Type', 
        choices=[
            ('pollution', 'Pollution'),
            ('habitat_loss', 'Habitat Loss'),
            ('illegal_activity', 'Illegal Activity'),
            ('wildlife_incident', 'Wildlife Incident'),
            ('other', 'Other')
        ],
        validators=[DataRequired()])
    severity = SelectField('Severity',
        choices=[
            ('Critical', 'Critical'),
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Low', 'Low')
        ],
        validators=[DataRequired()])
    title = StringField('Report Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    reporter_name = StringField('Reporter Name', validators=[DataRequired()])
    reporter_contact = StringField('Contact Information', validators=[DataRequired()])
    report_date = DateField('Report Date', validators=[DataRequired()])