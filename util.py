import data
from app import User, db


def create_user():
    for user in data.users:
        new_user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age_name=user['age_name'],
            email=user['email'],
            role=user['role'],
            phone=user['phone'],
        )
        db.session.add(new_user)
    db.session.commit()
