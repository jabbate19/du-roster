####################################
# File name: models.py             #
# Author: Joe Abbate               #
####################################
from doom import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=False)
    

    def __init__(self, id, email, name, rank, steamid, discordid):
        self.id = id
        self.email = email
        self.name = name
        self.rank = rank
        self.steamid = steamid
        self.discordid = discordid
