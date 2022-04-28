from os import environ as env

# Flask config
IP = env.get('IP', '0.0.0.0')
PORT = env.get('PORT', 8080)
SERVER_NAME = env.get('SERVER_NAME', 'light.csh.rit.edu')
PREFERRED_URL_SCHEME = env.get('PREFERRED_URL_SCHEME', 'https')

# DB Info
SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

# Openshift secret
SECRET_KEY = env.get("SECRET_KEY", default='SECRET-KEY')

# Google OpenID Connect SSO config
GOOGLE_ISSUER = env.get('GOOGLE_ISSUER', 'https://accounts.google.com')
GOOGLE_CLIENT_ID = env.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = env.get('GOOGLE_CLIENT_SECRET', '------')
