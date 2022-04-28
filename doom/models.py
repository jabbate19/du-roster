####################################
# File name: models.py             #
# Author: Joe Abbate               #
####################################
from doom import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'member'
    
    email = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=False)
    steamid = db.Column(db.String, primary_key=True, nullable=False)
    discordid = db.Column(db.String, nullable=True)

    def __init__(self, email, name, rank, steamid, discordid):
        self.email = email
        self.name = name
        self.rank = rank
        self.steamid = steamid
        self.discordid = discordid

    def __str__(self):
        return f"{self.rank} | {self.name} | {self.steamid} | {self.discordid} | {self.email}"

    def __repr__(self):
        return self.__str__()