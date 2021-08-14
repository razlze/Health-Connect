from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class PreferencesForm(FlaskForm):
  #creating input fields for form
  province = SelectField('Province', choices=[("ab", "Alberta"), ("bc", "British Columbia"), ("mb", "Manitoba"), ("nb", "New Brunswick"), ("nl", "Newfoundland & Labrador"), ("nt", "Northwest Territories"), ("ns", "Nova Scotia"), ("nu", "Nunavut"), ("on", "Ontario"), ("pei", "Prince Edward Island"), ("qu", "Quebec"), ("sk", "Saskatchewan"), ("yt", "Yukon Territories")], validators=[DataRequired()])
  facility = SelectField('Facility', choices=[("Ambulatory health care services", "Ambulatory care (including clinics)"), ("Hospitals", "Hospitals"), ("Nursing and residential care facilities", "Nursing & residential")], validators=[DataRequired()])
  wait_time = IntegerField('Max Wait Time (Hours)', validators=[DataRequired()])
  submit = SubmitField('Filter')