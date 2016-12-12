from app.models.SQL_DB import User, db


def edit_password(username, password):
    user = User.query.filter_by(username=username).first()
    user.password = password
    return db.session.commit()


def edit_mg_settings(username, mg_domain, mg_api_private, mg_sender):
    # print("2 MG Domain:", mg_domain, "MG API:", mg_api_private, "MG Sender:", mg_sender)
    # print("User:", username)
    user = User.query.filter_by(username=username).first()
    user.mg_domain = mg_domain
    user.mg_api_private = mg_api_private
    user.mg_sender = mg_sender
    return db.session.commit()