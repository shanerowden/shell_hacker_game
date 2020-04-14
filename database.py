from shellmancer import db
from shellmancer.models import *
from faker import Faker
from argon2 import PasswordHasher

def populate_test_users(db, num):
    fake = Faker()
    ph = PasswordHasher()
    hashed_pw = ph.hash("password")
    for i in range(num):
        if i == 0:
            user = UserAccount(email="admin@admin.com",
                               password=hashed_pw,
                               is_admin=True,
                               is_verified=True,
                               date_confirmed=datetime.utcnow())
        else:
            user = UserAccount(email=fake.email(),
                               password=hashed_pw,
                               is_over_18=fake.boolean())
        db.session.add(user)
        db.session.commit()

def drop_create(db):
    db.drop_all()
    db.create_all()
