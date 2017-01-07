from app.models.SQL_DB import Mailinglist, User, db


def create_mapping(user_email, user_email_md5, mailing_list_email):
	import hashlib

	try:
		mailing_list_created = Mailinglist.query.filter_by(user_email=user_email,
		                                                   mailing_list_email=mailing_list_email).first()

		if mailing_list_created is None:
			mailing_list_email_md5 = hashlib.md5(mailing_list_email.encode('utf-8')).hexdigest()
			mailing_list = Mailinglist('', user_email, user_email_md5, mailing_list_email, mailing_list_email_md5)
			db.session.add(mailing_list)
			db.session.commit()
			mailing_list_created = Mailinglist.query.filter_by(user_email_md5=user_email_md5,
			                                                   mailing_list_email_md5=mailing_list_email_md5).first()

		return mailing_list_created

	except Exception as inst:
		db.session.rollback()
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		mailing_list_created = Mailinglist.query.filter_by(user_email=user_email,
		                                                   mailing_list_email=mailing_list_email).first()
		return mailing_list_created


def add_mailing_list_member(user_email_md5, mailing_list_email_md5, member_email, ip_addr):
	from app.models.Mailgun_Internal import mailgun_api_add_group_member
	mailing_list = Mailinglist.query.filter_by(user_email_md5=user_email_md5,
	                                           mailing_list_email_md5=mailing_list_email_md5).first()
	username = mailing_list.user_email
	mailing_list = mailing_list.mailing_list_email
	user = User.query.filter_by(username=username).first()
	mg_api_private = user.mg_api_private
	result = mailgun_api_add_group_member(mg_api_private, mailing_list, member_email, ip_addr)
	return result


def get_mailing_list_mapping(mailing_list_id):
	mailing_list = Mailinglist.query.filter_by(id=mailing_list_id).first()
	print(mailing_list)
	return mailing_list
