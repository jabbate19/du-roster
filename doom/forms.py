from typing import Text
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, IntegerField, Form
from wtforms.validators import DataRequired
from .utils import RANK_LIST

class RecruitForm(FlaskForm):
    name = TextAreaField("Recruit's Name", validators=[DataRequired()])
    steamid = TextAreaField("Recruit's SteamID", validators=[DataRequired()])
    discordid = TextAreaField("Recruit's DiscordID", validators=[DataRequired()])
    email = TextAreaField("Recruit's Email", validators=[DataRequired()])
    new_rank = SelectField("Recruit's New Rank", choices=[rank[0] for rank in RANK_LIST], validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

class TrainingForm(FlaskForm):
    description = TextAreaField("Description of the Training", validators=[DataRequired()])
    number_in_attendance = IntegerField("Number of Troopers in Attendance", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

class AttendanceForm(FlaskForm):
    event = SelectField("Event Attended", validators=[DataRequired()])
    
    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

class EventLeadForm(FlaskForm):
    after_action = TextAreaField("Event After-Action Report", validators=[DataRequired()])
    number_in_attendance = IntegerField("Number of Troopers in Attendance", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

class ObserveForm(FlaskForm):
    observee = SelectField("Person Being Observed", validators=[DataRequired()])
    event_type = SelectField("Type of Event Being Observed", choices=[("training", "Training"), ("recruitment", "Recruitment")])
    rating = IntegerField("Rating from 1-10", validators=[DataRequired()])
    notes = TextAreaField("Any Notes from the Observation", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True

class PromoteForm(FlaskForm):
    promotee = SelectField("Person Being Promoted/Demoted", validators=[DataRequired()])
    new_rank = SelectField("Rank Being Promoted To", validators=[DataRequired()])
    reason = TextAreaField("Reason", validators=[DataRequired()])
    
    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not Form.validate(self, extra_validators=extra_validators):
            return False
        return True