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
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import time



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
socketio = SocketIO(app)

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
from .models import User, Room
from .forms import ColorForm, RoomForm
from .utils import csh_user_auth

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
    q = User.query.get(user_id)
    if q:
        return q
    return None

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
    ranks = {
        "CMD": filter(lambda member: member.rank == "CMD", members),
        "XO": filter(lambda member: member.rank == "XO", members),

        "COL": filter(lambda member: member.rank == "COL", members),
        "LTC": filter(lambda member: member.rank == "LTC", members),
        "MAJ": filter(lambda member: member.rank == "MAJ", members),

        "CPT": filter(lambda member: member.rank == "CPT", members),
        "1stLT": filter(lambda member: member.rank == "1stLT", members),
        "2ndLT": filter(lambda member: member.rank == "2ndLT", members),

        "SMB": filter(lambda member: member.rank == "SMB", members),

        "CSM": filter(lambda member: member.rank == "CSM", members),
        "SGM": filter(lambda member: member.rank == "SGM", members),
        "1SG": filter(lambda member: member.rank == "1SG", members),
        "MSG": filter(lambda member: member.rank == "MSG", members),
        "SFC": filter(lambda member: member.rank == "SFC", members),
        "SSG": filter(lambda member: member.rank == "SSG", members),
        "SGT": filter(lambda member: member.rank == "SGT", members),

        "CPL": filter(lambda member: member.rank == "CPL", members),
        "LCPL": filter(lambda member: member.rank == "LCPL", members),
        "PFC": filter(lambda member: member.rank == "PFC", members),
        "PVT": filter(lambda member: member.rank == "PVT", members)
    }
    
    return render_template('roster.html', ranks=ranks, commit=commit)

