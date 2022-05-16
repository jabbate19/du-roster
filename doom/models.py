####################################
# File name: models.py             #
# Author: Joe Abbate               #
####################################
from doom import db
from datetime import datetime
from sys import stderr

class Member(db.Model):
    __tablename__ = 'member'
    
    steamid = db.Column(db.String, primary_key=True, nullable=False)
    discordid = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=False)
    lore_name = db.Column(db.String, nullable=True)

    def __init__(self, email, name, rank, steamid, discordid):
        self.steamid = steamid
        self.discordid = discordid
        self.email = email
        self.name = name
        self.rank = rank
        
    def __str__(self):
        return f"{self.rank} | {self.name} | {self.steamid} | {self.discordid} | {self.email}"

    def __repr__(self):
        return self.__str__()

class Recruitment(db.Model):
    __tablename__ = 'recruitment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    recruiter = db.Column(db.String, nullable=False)
    recruitee = db.Column(db.String, nullable=False)
    new_rank = db.Column(db.String, nullable=False)

    def __init__(self, recruiter, recruitee, new_rank):
        self.recruiter = recruiter
        self.recruitee = recruitee
        self.new_rank = new_rank

class Training(db.Model):
    __tablename__ = 'training'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    trainer = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    number_in_attendance = db.Column(db.Integer, nullable=False)

    def __init__(self, trainer, description, number_in_attendance):
        self.trainer = trainer
        self.description = description
        self.number_in_attendance = number_in_attendance

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    attendee = db.Column(db.String, nullable=False)
    event_type = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)

    def __init__(self, attendee, event_type, event_id):
        self.attendee = attendee
        self.event_type = event_type
        self.event_id = event_id

class Event_Lead(db.Model):
    __tablename__ = 'eventlead'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    leader = db.Column(db.String, nullable=False)
    after_action = db.Column(db.String, nullable=False)
    number_in_attendance = db.Column(db.Integer, nullable=False)

    def __init__(self, leader, after_action, number_in_attendance):
        self.leader = leader
        self.after_action = after_action
        self.number_in_attendance = number_in_attendance

class LOA_ROA(db.Model):
    __tablename__ = 'absence'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    member = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)

class Promotion(db.Model):
    __tablename__ = 'promotion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    promoter = db.Column(db.String, nullable=False)
    promotee = db.Column(db.String, nullable=False)
    old_rank = db.Column(db.String, nullable=False)
    new_rank = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)

    def __init__(self, promoter, promotee, old_rank, new_rank, reason):
        self.promoter = promoter
        self.promotee = promotee
        self.old_rank = old_rank
        self.new_rank = new_rank
        self.reason = reason

class Observation(db.Model):
    __tablename__ = 'observation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    observer = db.Column(db.String, nullable=False)
    observee = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String, nullable=False)

    def __init__(self, observer, observee, type, rating, notes):
        self.observer = observer
        self.observee = observee
        self.type = type
        self.rating = rating
        self.notes = notes

class Strike(db.Model):
    __tablename__ = 'strike'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    officer = db.Column(db.String, nullable=False)
    receiving = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)

class Points(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    recruitment = db.Column(db.Float, nullable=False)
    training = db.Column(db.Float, nullable=False)
    attendance = db.Column(db.Float, nullable=False)
    overseer = db.Column(db.Float, nullable=False)
    subdivision = db.Column(db.Float, nullable=False)