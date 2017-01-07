# -*- coding: utf-8 -*-
from flask import render_template, session, request, redirect, url_for

from app import app
from app.models.Login import login_required


@app.route('/mailing_lists', methods=['GET'])
@login_required
def mailing_lists_index():
	from app.models.Mailgun_Internal import mailgun_get_groups
	mailing_lists = mailgun_get_groups()
	return render_template('mailing_lists/index.html', mailing_lists=mailing_lists)


@app.route('/mailing_lists/add', methods=['GET'])
@login_required
def mailing_lists_add():
	mg_domain = session['mg_domain']
	return render_template('mailing_lists/add.html', mg_domain=mg_domain)


@app.route('/mailing_lists/submit', methods=['POST'])
@login_required
def mailing_lists_submit():
	from app.models.Mailgun_Internal import mailgun_create_group
	address = request.form['address']
	name = request.form['name']
	description = request.form['description']
	mailgun_create_group(address, name, description)
	return redirect(url_for('mailing_lists_index'))


@app.route('/mailing_lists/edit/<mailing_list_id>', methods=['GET'])
@login_required
def mailing_lists_edit(mailing_list_id):
	from app.models.Mailgun_Internal import mailgun_get_group, mailgun_get_group_members
	address = mailing_list_id.replace("%40", "@")
	mg_data = mailgun_get_group(address)
	members = mailgun_get_group_members(address)
	return render_template('mailing_lists/edit.html', mg_data=mg_data, members=members)


@app.route('/mailing_lists/edit/<mailing_list_id>/members', methods=['GET'])
@login_required
def mailing_lists_edit_members(mailing_list_id):
	from app.models.Mailgun_Internal import mailgun_get_group, mailgun_get_group_members
	address = mailing_list_id.replace("%40", "@")
	mg_data = mailgun_get_group(address)
	members = mailgun_get_group_members(address)
	return render_template('mailing_lists/members.html', mg_data=mg_data, members=members)


@app.route('/mailing_lists/edit/<mailing_list_id>/mapper', methods=['GET'])
@login_required
def mailing_lists_edit_mapper(mailing_list_id):
	from app.models.Mailing_Lists import create_mapping
	user_email = session['username']
	user_email_md5 = session['gravatar']
	mailing_list_email = mailing_list_id
	result = create_mapping(user_email, user_email_md5, mailing_list_email)
	# print(result.id)
	form_template = render_template('mailing_lists/form.html', mailing_list=result, app_domain=app.config['APP_DOMAIN'])
	# print(form_template)
	return render_template('mailing_lists/mapper.html', mailing_list_email=mailing_list_email, user_email=user_email,
	                       user_email_md5=user_email_md5, creation_result=result, form_template=form_template)


@app.route('/mailing_lists/delete/<mailing_list_id>', methods=['GET'])
@login_required
def mailing_lists_delete(mailing_list_id):
	from app.models.Mailgun_Internal import mailgun_delete_group
	address = mailing_list_id.replace("%40", "@")
	mailgun_delete_group(address)
	return redirect(url_for('mailing_lists_index'))


@app.route('/mailing_lists/api', methods=['GET', 'POST'])
def mailing_lists_api():
	from app.models.Settings import get_user_ip
	from app.models.Mailing_Lists import add_mailing_list_member, get_mailing_list_mapping
	referer = request.headers.get("Referer")
	# print(referer)

	if request.method == 'POST':
		user_email_md5 = request.form['user_email']
		mailing_list_email_md5 = request.form['mailing_list_email']
		member_email = request.form['member_email']
		ip_addr = get_user_ip()
		response = add_mailing_list_member(user_email_md5, mailing_list_email_md5, member_email, ip_addr)
		# print(response)
		# return str(response)
		return redirect(referer)

	elif request.method == 'GET':
		app_domain = app.config['APP_DOMAIN']
		ml_id = request.args.get('id') or None
		if ml_id:
			mailing_list = get_mailing_list_mapping(ml_id)
			return render_template('mailing_lists/form.html', mailing_list=mailing_list, app_domain=app_domain)
		else:
			return "No Form ID"

	else:
		return "Bad Request"
