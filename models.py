from app import db
from datetime import datetime

# Models
class UserAccount(db.Model):
    """
    Account Holding User
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="static/default.jpg")
    password = db.Column(db.String(60), nullable=False)
    account_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    agree_over_18 = db.Column(db.Boolean, default=False)

    player = db.relationship('PlayerProfile', uselist=False, back_populates="user")

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"

    def __init__(self, **kwargs):
        super(UserAccount, self).__init__(**kwargs)

        db.session.add(self)
        db.session.commit()

        new_player = PlayerProfile(id=self.id)

        db.session.add(new_player)
        db.session.commit()

class PlayerProfile(db.Model):
    """
    Each user gets a player profile with which to make characters
    and save progress in various Campaigns
    """
    __tablename__ = 'player'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    user = db.relationship('UserAccount', back_populates="player")

    def __repr__(self):
        return f"PlayerProfile({self.id}, {self.user})"


class GameMasterProfile(db.Model):
    """
    Can create campaigns, view characters playing their campaigns...
    For now, unavailable except to developer
    """
    id = db.Column(db.Integer, primary_key=True)
    # campaigns = db.relationship('SinglePlayerCampaign', backref='GM', lazy=True)


class SinglePlayerCampaign(db.Model):
    """
    Created by one user with GameMasterProfile
    Anyone with PlayerProfile may make a character to play the campaign.
    """
    id = db.Column(db.Integer, primary_key=True)


class CharacterSheet(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)

