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
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import time
import sys


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
from .models import Member
from .utils import google_user_auth
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
    members = list(Member.query.all())
    print("Members:", members, file=sys.stderr)
    rank_list = [
        ("CMD", "COMMANDER DOOM"),
        ("XO", "EXECUTIVE OFFICER"),
        ("COL", "COLONEL"),
        ("LTC", "LIEUTENANT COLONEL"),
        ("MAJ", "MAJOR"),
        ("CPT", "CAPTAIN"),
        ("1stLT", "FIRST LIEUTENANT"),
        ("2ndLT", "SECOND LIEUTENANT"),
        ("SMB", "SERGEANT MAJOR OF THE BATTALION"),
        ("CSM", "COMMAND SERGEANT MAJOR"),
        ("SGM", "SERGEANT MAJOR"),
        ("1SG", "FIRST SERGEANT"),
        ("MSG", "MASTER SERGEANT"),
        ("SFC", "SERGEANT FIRST CLASS"),
        ("SSG", "STAFF SERGEANT"),
        ("SGT", "SERGEANT"),
        ("CPL", "CORPORAL"),
        ("LCPL", "LANCE CORPORAL"),
        ("PFC", "PRIVATE FIRST CLASS"),
        ("PVT", "PRIVATE")
    ]
    ranks = {}
    for rank in rank_list:
        ranks[rank[0]] = list(filter(lambda member: member.rank==rank[0], members))
        print(rank,list(ranks[rank[0]]), file=sys.stderr)
    return render_template('roster.html', xo=ranks["XO"], rank_list=rank_list, ranks=ranks, commit=commit)

