from shellmancer import db
from shellmancer.models import *
from faker import Faker

def populate_test_users(db, num):
    fake = Faker()
    for i in range(num):
        if i == 0:
            user = UserAccount(email="admin@admin.com",
                               password="password",
                               is_admin=True)
        else:
            user = UserAccount(email=fake.email(),
                               password=fake.password(),
                               agree_over_18=fake.boolean())
        db.session.add(user)
        db.session.commit()

def drop_create(db):
    db.drop_all()
    db.create_all()

