####################################
# File name: __init__.py           #
# Author: Joe Abbate               #
####################################
from subprocess import check_output
from datetime import datetime
import os
import socket
import pytz
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask import Flask, render_template, send_from_directory, redirect, url_for, g, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import time
import sys

from .forms import *


# Setting up Flask and csrf token for forms.
app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

# Establish SQL Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# OIDC Authentication
GOOGLE_AUTH = ProviderConfiguration(issuer=app.config["GOOGLE_ISSUER"],
                                    client_metadata=ClientMetadata(
                                        app.config["GOOGLE_CLIENT_ID"],
                                        app.config["GOOGLE_CLIENT_SECRET"]), 
                                    auth_request_params={'scope': ['email', 'profile', 'openid']})
auth = OIDCAuthentication({'default': GOOGLE_AUTH},
                          app)

auth.init_app(app)

# Flask-Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Commit
commit = check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').rstrip()

# pylint: disable=wrong-import-position
from .models import *
from .utils import RANK_VALUE, google_user_auth, RANK_LIST
from .user import User

# time setup for the server side time
eastern = pytz.timezone('America/New_York')
fmt = '%Y-%m-%d %H:%M'

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/assets'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/logout")
@auth.oidc_logout
def _logout():
    logout_user()
    return redirect("/", 302)

@app.route('/login')
@app.route('/')
@auth.oidc_auth('default')
@google_user_auth
def google_auth(auth_dict=None):
    if auth_dict is None:
        return redirect(url_for('login'))
    user = User(auth_dict['email'])
    login_user(user)
    return redirect(url_for('index'))

# Application
@app.route('/roster')
@login_required
def index():
    members = db.session.execute(text(
        """
        SELECT member.name, member.lore_name, member.steamid, COALESCE(promo_date, recruit_date),
            COALESCE(recruitments, 0) AS recruitments,
            COALESCE(trainings, 0) AS trainings,
            COALESCE(attendances, 0) AS attendances,
            COALESCE(leads, 0) AS leads,
            COALESCE(observations, 0) AS observations,
            member.discordid,
            COALESCE(strikes, 0) AS strikes,
            member.rank
        FROM member
        LEFT JOIN (
            SELECT recruiter, COUNT(*) AS recruitments
                FROM recruitment
                GROUP BY recruiter
        ) recruitment_count ON recruitment_count.recruiter = member.steamid
        LEFT JOIN (
            SELECT trainer, COUNT(*) AS trainings
                FROM training
                GROUP BY trainer
        ) training_count ON training_count.trainer = member.steamid
        LEFT JOIN(
            SELECT attendee, COUNT(*) AS attendances
                FROM attendance
                GROUP BY attendee
        ) attendance_count ON attendance_count.attendee = member.steamid
        LEFT JOIN (
            SELECT leader, COUNT(*) AS leads
                FROM eventlead
                GROUP BY leader
        ) lead_count ON lead_count.leader = member.steamid
        LEFT JOIN (
            SELECT observer, COUNT(*) AS observations
                FROM observation
                GROUP BY observer
        ) obs_count ON obs_count.observer = member.steamid
        LEFT JOIN (
            SELECT receiving, COUNT(*) AS strikes
                FROM strike
                GROUP BY receiving
        ) strike_count ON strike_count.receiving = member.steamid
		LEFT JOIN (
            SELECT promotee, MAX(timestamp) as promo_date
                FROM promotion
                GROUP BY promotee
        ) promotions_dates ON promotions_dates.promotee = member.steamid
		LEFT JOIN (
            SELECT recruitee, MAX(timestamp) as recruit_date
                FROM recruitment
                GROUP BY recruitee
        ) recruit_date ON recruit_date.recruitee = member.steamid
        """
    ))
    points = Points.query.all()[0]
    
    ranks = {}
    members = list(members)
    for tag, name in RANK_LIST:
        ranks[tag] = list(map(lambda member: get_member_info(member, points), filter(lambda member: member[11]==tag, members)))
    return render_template('roster.html', rank_list=RANK_LIST, ranks=ranks, commit=commit)

@app.route('/recruit', methods=["GET", "POST"])
@login_required
def recruit():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    form = RecruitForm()
    if form.validate_on_submit():
        trooper = Member(form.email.data, form.name.data, form.new_rank.data, form.steamid.data, form.discordid.data)
        recruitment = Recruitment(member.steamid, trooper.steamid, form.new_rank.data)
        db.session.add(trooper)
        db.session.add(recruitment)
        db.session.commit()
        return redirect('/roster')
    return render_template('recruit.html', form=form, commit=commit)

@app.route('/train', methods=["GET", "POST"])
@login_required
def train():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    form = TrainingForm()
    if form.validate_on_submit():
        training = Training(member.steamid, form.description.data, form.number_in_attendance.data)
        db.session.add(training)
        db.session.commit()
        return redirect('/roster')
    return render_template('train.html', form=form, commit=commit)

@app.route('/lead', methods=["GET", "POST"])
@login_required
def lead():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    form = EventLeadForm()
    if form.validate_on_submit():
        lead = Event_Lead(member.steamid, form.after_action.data, form.number_in_attendance.data)
        db.session.add(lead)
        db.session.commit()
        return redirect('/roster')
    return render_template('lead.html', form=form, commit=commit)

@app.route('/attend', methods=["GET", "POST"])
@login_required
def attendance():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    form = AttendanceForm()
    form.event.choices = []
    if form.validate_on_submit():
        event_type, event_id = form.event.data
        attendance = Attendance(member.steamid, event_type, event_id)
        db.session.add(attendance)
        db.session.commit()
        return redirect('/roster')
    return render_template('attend.html', form=form, commit=commit)

@app.route('/observe', methods=["GET", "POST"])
@login_required
def observe():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    member_list = Member.query.order_by(Member.name).all()
    form = ObserveForm()
    form.observee.choices = [(m.steamid, m.name) for m in member_list]
    if form.validate_on_submit():
        observation = Observation(member.steamid, form.observee.data, form.event_type.data, form.rating.data, form.notes.data)
        db.session.add(observation)
        db.session.commit()
        return redirect('/roster')
    return render_template('observe.html', form=form, commit=commit)

@app.route('/promote', methods=["GET", "POST"])
@login_required
def promote():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    member_list = Member.query.order_by(Member.name).all()
    form = PromoteForm()
    form.promotee.choices = [(m.steamid, f"{m.rank} {m.name}") for m in sorted(member_list, key=lambda mem: RANK_VALUE[mem.rank], reverse=True)]
    form.new_rank.choices = [(rank[0], f"{rank[1]} ({rank[0]})") for rank in RANK_LIST]
    if form.validate_on_submit():
        promotee = form.promotee.data
        new_rank = form.new_rank.data
        reason = form.reason.data
        promotion = Promotion(member.steamid, promotee.steamid, promotee.rank, new_rank, reason)
        db.session.add(promotion)
        db.session.commit()
        promotee.rank = new_rank
        db.session.commit()
        return redirect('/roster')
    return render_template('promote.html', form=form, commit=commit)

@app.route('/strike', methods=["GET", "POST"])
@login_required
def strike():
    member = Member.query.filter(Member.email==current_user.email).first()
    if not member:
        abort(403)
    form = TrainingForm()
    if form.validate_on_submit():
        training = Training(member.steamid, form.description.data, form.number_in_attendance.data)
        db.session.add(training)
        db.session.commit()
        return redirect('/roster')
    return render_template('train.html', form=form, commit=commit)

def get_member_info(member, points):
    point_total = (member[4]*points.recruitment)
    point_total += (member[5]*points.training)
    point_total += (member[6]*points.attendance)
    point_total += (member[7]*points.overseer)
    point_total += (0*points.subdivision)
    
    date_str = member[3]
    date = ""
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f").strftime("%m/%d/%Y")
    return (member, point_total,date)