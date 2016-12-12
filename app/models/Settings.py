from app.models.SQL_DB import User, db
from flask import session


def edit_password(password):
    username = session['username']
    user = User.query.filter_by(username=username).first()
    user.password = password
    return db.session.commit()


def edit_mg_settings(mg_domain, mg_api_private, mg_sender):
    username = session['username']
    user = User.query.filter_by(username=username).first()
    user.mg_domain = mg_domain
    user.mg_api_private = mg_api_private
    user.mg_sender = mg_sender
    return db.session.commit()