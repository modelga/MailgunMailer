import json

from flask_bcrypt import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from app import app

db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True)
	password = db.Column(db.Text)
	name_1 = db.Column(db.Text)
	name_2 = db.Column(db.Text)
	company = db.Column(db.Text)
	address = db.Column(db.Text)
	mg_api_private = db.Column(db.Text)
	mg_domain = db.Column(db.Text)
	mg_sender = db.Column(db.Text)
	email_md5 = db.Column(db.Text)
	admin = db.Column(db.Boolean, unique=False, default=False, nullable=False)

	def __init__(self, id, username, password, name_1, name_2, company, address, mg_api_private, mg_domain, mg_sender,
	             email_md5, admin):
		self.id = id
		self.username = username
		self.password = password
		self.name_1 = name_1
		self.name_2 = name_2
		self.company = company
		self.address = address
		self.mg_api_private = mg_api_private
		self.mg_domain = mg_domain
		self.mg_sender = mg_sender
		self.email_md5 = email_md5
		self.admin = admin

	def __repr__(self):
		json_data = json.dumps(
			{"id": self.id, "username": self.username, "password": self.password, "name_1": self.name_1,
			 "name_2": self.name_2, "company": self.company, "address": self.address,
			 "mg_api_private": self.mg_api_private,
			 "mg_domain": self.mg_domain, "mg_sender": self.mg_sender, "email_md5": self.email_md5, "admin": self.admin}
			, sort_keys=True)
		return json_data


class Newsletter(db.Model):
	__tablename__ = 'newsletters'

	id = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(255), db.ForeignKey('users.username'))
	recipients = db.Column(db.Text)
	message = db.Column(db.Text)
	creation_date = db.Column(db.DateTime)
	mg_id = db.Column(db.Text)
	mg_status = db.Column(db.Boolean)
	subject = db.Column(db.Text)
	sender = db.Column(db.Text)
	tags = db.Column(db.Text)
	campaign = db.Column(db.Text)

	def __init__(self, id, username, recipients, message, creation_date, mg_id, mg_status, subject, sender, tags,
	             campaign):
		self.id = id
		self.username = username
		self.recipients = recipients
		self.message = message
		if creation_date is None:
			from datetime import datetime
			creation_date = datetime.now()
		self.creation_date = creation_date
		self.mg_id = mg_id
		self.mg_status = mg_status
		self.subject = subject
		self.sender = sender
		self.tags = tags
		self.campaign = campaign

	def __repr__(self):
		json_data = json.dumps(
			{"id": self.id, "username": self.username, "recipients": self.recipients, "message": self.message,
			 "creation_date": str(self.creation_date), "mg_id": self.mg_id, "mg_status": self.mg_status,
			 "subject": self.subject,
			 "sender": self.sender, "tags": self.tags, "campaign": self.campaign}
			, sort_keys=True)
		return json_data


class Mailinglist(db.Model):
	__tablename__ = 'mailinglists'

	id = db.Column(db.Integer, primary_key=True, unique=True)
	user_email = db.Column(db.String(255), db.ForeignKey('users.username'))
	user_email_md5 = db.Column(db.String(255))
	mailing_list_email = db.Column(db.String(255))
	mailing_list_email_md5 = db.Column(db.String(255))
	UniqueConstraint('user_email', 'mailing_list_email', name='unique_emails')

	def __init__(self, id, user_email, user_email_md5, mailing_list_email, mailing_list_email_md5):
		self.id = id
		self.user_email = user_email
		self.user_email_md5 = user_email_md5
		self.mailing_list_email = mailing_list_email
		self.mailing_list_email_md5 = mailing_list_email_md5

	def __repr__(self):
		json_data = json.dumps(
			{"id": self.id, "user_email": self.user_email, "user_email_md5": self.user_email_md5,
			 "mailing_list_email": self.mailing_list_email,
			 "mailing_list_email_md5": self.mailing_list_email_md5}
			, sort_keys=True)
		return json_data


def auth_user(username, password):
	try:
		password_hash = User.query.filter_by(username=username).first()
		password_hash = password_hash.password
		pw_result = check_password_hash(str(password_hash), str(password))
		return pw_result
	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		return False
