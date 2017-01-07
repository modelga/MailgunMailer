# -*- coding: utf-8 -*-
from flask import render_template, session, request, redirect, url_for

from app import app
from app.models.Login import login_required
from app.models.SQL_DB import Newsletter


@app.route('/newsletters', methods=['GET', 'POST'])
@login_required
def newsletters_index():
    from app.models.Newsletters import user_newsletters
    username = session['username']
    user_newsletters = user_newsletters(username)
    return render_template('newsletters/index.html', user_newsletters=user_newsletters)


@app.route('/newsletters/add', methods=['GET', 'POST'])
@login_required
def newsletters_add():
    from app.models.Mailgun_Internal import mailgun_get_groups, mailgun_get_campaigns
    app_domain = app.config['APP_DOMAIN']
    mg_sender = session['mg_sender']
    mailgun_campaigns = mailgun_get_campaigns()
    recipients = mailgun_get_groups()
    return render_template('newsletters/add.html', recipients=recipients, mailgun_campaigns=mailgun_campaigns,
                           mg_sender=mg_sender, app_domain=app_domain)


@app.route('/newsletters/edit/<newsletter_id>', methods=['GET', 'POST'])
@login_required
def newsletters_edit(newsletter_id):
    from app.models.Newsletters import edit_newsletter
    from app.models.Mailgun_Internal import mailgun_get_groups, mailgun_get_campaigns
    app_domain = app.config['APP_DOMAIN']
    username = session['username']
    mg_sender = session['mg_sender']
    recipients = mailgun_get_groups()
    newsletter_data = edit_newsletter(newsletter_id)
    mailgun_campaigns = mailgun_get_campaigns()
    try:
        newsletter_username = Newsletter.query.filter_by(username=username, id=newsletter_id).first().username
    except:
        newsletter_username = "Bad Value"
    if username == newsletter_username:
        return render_template('newsletters/edit.html', newsletter_data=newsletter_data, mg_sender=mg_sender,
                               username=username, recipients=recipients, mailgun_campaigns=mailgun_campaigns, app_domain=app_domain)
    else:
        return redirect(url_for('newsletters_index'))


@app.route('/newsletters/delete/<newsletter_id>', methods=['GET', 'POST'])
@login_required
def newsletters_delete(newsletter_id):
    from app.models.Newsletters import delete_newsletter
    try:
        delete_newsletter(newsletter_id)
        return redirect(url_for('newsletters_index'))
    except:
        return "Problem occurred. Contact system administrator"


@app.route('/newsletters/submit', methods=['GET', 'POST'])
@login_required
def newsletters_submit():
    from app.models.Newsletters import add_newsletter, edit_add_newsletter
    subject = request.form['subject']
    message = request.form['message']
    recipients = request.form['recipients']
    sender = request.form['sender']
    tags = request.form['tags']
    campaign = request.form['campaign']
    username = session['username']

    try:
        update = request.form['update']
    except:
        update = 'False'

    if update == 'True':
        newsletter_id = request.form['newsletter_id']
        edit_add_newsletter(username, subject, message, recipients, sender, tags, campaign, newsletter_id)
    else:
        add_newsletter(username, subject, message, recipients, sender, tags, campaign)

    return redirect(url_for('newsletters_index'))


@app.route('/newsletters/send', methods=['POST'])
@login_required
def newsletters_send():
    from app.models.Newsletters import send_newsletter, update_newsletter_status
    newsletter_id = request.form['newsletter_id']
    mailgun_response = send_newsletter(newsletter_id)
    update_newsletter_status(mailgun_response, newsletter_id)
    return str(mailgun_response['message'])
