from flask import session

from app.models.SQL_DB import User, db


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


def get_user_ip():
	from flask import request
	try:
		user_ip = request.access_route[0]
	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
		print("Alternative IP:", user_ip)

	return user_ip
