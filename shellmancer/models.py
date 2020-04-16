from shellmancer import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.dialects.postgresql import JSONB


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))


# Models
class UserAccount(db.Model, UserMixin):
    """
    UserAccount 1-1 PlayerProfile
    UserAccount 1-1 GameMasterProfile
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    password = db.Column(db.String(77), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_confirmed = db.Column(db.DateTime, nullable=True)
    is_over_18 = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_email_public = db.Column(db.Boolean, nullable=False, default=False)
    has_seen_tutorial = db.Column(db.Boolean, default=False)

    player = db.relationship('PlayerProfile', uselist=False, back_populates="user")
    gamemaster = db.relationship('GameMasterProfile', uselist=False, back_populates="user")

    def get_token(self, expires_sec):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
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
        new_player = PlayerProfile(id=self.id)
        new_gm = GameMasterProfile(id=self.id)

        # Commit to DB
        db.session.add(new_player)
        db.session.add(new_gm)
        db.session.commit()


class PlayerProfile(db.Model):
    """
    PlayerProfile 1-M CharacterSheet
    UserAccount 1-1 PlayerProfile
    """
    __tablename__ = 'player'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    access = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('UserAccount', back_populates="player")
    characters = db.relationship('CharacterSheet', back_populates="player")

    def __repr__(self):
        return f"PlayerProfile({self.id}, {self.user})"


class GameMasterProfile(db.Model):
    """
    UserAccount 1-1 PlayerProfile
    GameMasterProfile 1-M SinglePlayerCampaign
    """
    __tablename__ = 'gamemaster'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    access = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship('UserAccount', back_populates="gamemaster")
    campaigns = db.relationship('SinglePlayerCampaign', back_populates="gamemaster")

    def __repr__(self):
        return f"GameMasterProfile({self.id}, {self.user})"

#
class CharacterSheet(db.Model):
    """
    CharacterSheet M-1 PlayerProfile
    CharacterSheet 1-1 SinglePlayerCampaign
    """
    __tablename__ = 'character_sheet'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    attr_a = db.Column(db.Integer)
    attr_b = db.Column(db.Integer)
    attr_c = db.Column(db.Integer)

    player = db.relationship('PlayerProfile', back_populates='characters')
    campaign = db.relationship('SinglePlayerCampaign', back_populates="character_sheet")


class SinglePlayerCampaign(db.Model):
    """
    CharacterSheetr 1-1 SinglePlayerCampaign
    GameMasterProfile 1-M SinglePlayerCampaign
    """
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    descrip = db.Column(db.String(250), nullable=False)  # tagline
    intro_text = db.Column(db.String(2800))
    gamemaster_id = db.Column(db.Integer, db.ForeignKey('gamemaster.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    date_published = db.Column(db.DateTime, default=datetime.utcnow)
    has_adult_content = db.Column(db.Boolean, default=False)


    attr_a_name = db.Column(db.String(25))
    attr_b_name = db.Column(db.String(25))
    attr_c_name = db.Column(db.String(25))
    attr_a_descrip = db.Column(db.String(250))
    attr_b_descrip = db.Column(db.String(250))
    attr_c_descrip = db.Column(db.String(250))

    gamemaster = db.relationship('GameMasterProfile', back_populates="campaigns")
    character_sheet = db.relationship("CharacterSheet", back_populates="campaign")
