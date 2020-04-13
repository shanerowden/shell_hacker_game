from shellmancer import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))


# Models
class UserAccount(db.Model, UserMixin):
    """
    Account Holding Base User.
    This class is the bassis both GameMasterProfile and PlayerProfile.
    It should be a strictly one to one relationship.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_confirmed = db.Column(db.DateTime, nullable=True)
    is_over_18 = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)

    player = db.relationship('PlayerProfile', uselist=False, back_populates="user")
    gamemaster = db.relationship('GameMasterProfile', uselist=False, back_populates="user")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserAccount.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"

    def __init__(self, **kwargs):
        super(UserAccount, self).__init__(**kwargs)

        # Create Row in DB When Created
        db.session.add(self)
        db.session.commit()

        # Apply a player/gamemaster profile to users on creation
        new_player = PlayerProfile(player_id=self.id)
        new_gm = GameMasterProfile(gamemaster_id=self.id)

        # Commit to DB
        db.session.add(new_player)
        db.session.add(new_gm)
        db.session.commit()



class PlayerProfile(db.Model):
    """
    Each user gets a player profile with which to make characters
    and save progress in various Campaigns.
    """
    __tablename__ = 'player'

    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    player_access = db.Column(db.Integer, nullable=False, default=1)
    user = db.relationship('UserAccount', back_populates="player")
    # characters = db.relationship('CharacterSheet', backref="player")

    def __repr__(self):
        return f"PlayerProfile({self.player_id}, {self.user})"


class GameMasterProfile(db.Model):
    """
    Can create campaigns, view characters playing their campaigns...
    For now, unavailable except to developer. Both this class and the PlayerProfile are created on
    New User init, but their access prolperties vary.
    """
    __tablename__ = 'gamemaster'

    gamemaster_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    gamemaster_access = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('UserAccount', back_populates="gamemaster")
    campaigns = db.relationship('SinglePlayerCampaign', backref="gamemaster")

    def __repr__(self):
        return f"GameMasterProfile({self.gamemaster_id}, {self.user})"


class CharacterSheet(db.Model):
    """

    """
    __tablename__ = 'character_sheet'

    character_sheet_id = db.Column(db.Integer, primary_key=True)


class SinglePlayerCampaign(db.Model):
    """
    Created by one user with GameMasterProfile
    Anyone with PlayerProfile may make a character to play the campaign.
    """
    __tablename__ = 'campaign'

    campaign_id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(120), nullable=False)
    campaign_descrip = db.Column(db.String(250), nullable=False)
    gamemaster_id = db.Column(db.Integer, db.ForeignKey('gamemaster.gamemaster_id'), nullable=False)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.character_sheet_id'))