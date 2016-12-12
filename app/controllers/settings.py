# -*- coding: utf-8 -*-
from flask import render_template, session, request

from app import app
from app.models.Login import login_required
from app.models.SQL_DB import User


@app.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def settings_profile():
    from app.models.Mailgun_Internal import mailgun_get_campaigns
    username = session['username']
    campaigns = mailgun_get_campaigns()
    user_data = User.query.filter_by(username=username).first()
    return render_template('settings/index.html', user_data=user_data, campaigns=campaigns)


@app.route('/settings/profile/pw_change', methods=['POST'])
@login_required
def settings_profile_pw_change():
    from app.models.Settings import edit_password
    from flask_bcrypt import generate_password_hash

    try:
        password = request.form['password']
        username = session['username']
        pw_hash = generate_password_hash(password).decode('utf8')
        edit_password(username, pw_hash)

        return "Success. Password Changed."
    except:
        return "Problem occurred. Contact system administrator"


@app.route('/settings/profile/mg_change', methods=['POST'])
@login_required
def settings_profile_mg_change():
    from app.models.Settings import edit_mg_settings
    try:
        username = session['username']
        mg_domain = request.form['mg_domain']
        mg_api_private = request.form['mg_api_private']
        mg_sender = request.form['mg_sender']
        edit_mg_settings(username, mg_domain, mg_api_private, mg_sender)
        return "Success. Settings Changed."
    except:
        return "Problem occurred. Contact system administrator"


@app.route('/settings/campaigns/add', methods=['POST'])
@login_required
def settings_campaigns_add():
    from app.models.Mailgun_Internal import mailgun_add_campaigns

    try:
        campaign_name = request.form['campaign_name']
        mailgun_add_campaigns(campaign_name)
        return "Success. Campaign added."
    except:
        return "Problem occurred. Contact system administrator"


@app.route('/settings/campaigns/delete', methods=['POST'])
@login_required
def settings_campaigns_delete():
    from app.models.Mailgun_Internal import mailgun_delete_campaigns

    try:
        campaign_name = request.form['campaign_name']
        mailgun_delete_campaigns(campaign_name)
        return "Success. Campaign Deleted."
    except:
        return "Problem occurred. Contact system administrator"
