from flask import session

from app.models.SQL_DB import Newsletter, db


def user_newsletters(email):
    newsletters = Newsletter.query.filter_by(username=email).all()
    return newsletters


def add_newsletter(username, subject, message, recipients, sender, tags, campaign):
    newsletter = Newsletter(None, username, recipients, message, None, None, 0, subject, sender, tags, campaign)
    db.session.add(newsletter)
    return db.session.commit()


def edit_add_newsletter(username, subject, message, recipients, sender, tags, campaign, newsletter_id):
    newsletter = Newsletter.query.filter_by(username=username, id=newsletter_id).first()
    newsletter.subject = subject
    newsletter.message = message
    newsletter.recipients = recipients
    newsletter.sender = sender
    newsletter.tags = tags
    newsletter.campaign = campaign
    return db.session.commit()


def send_newsletter(newsletter_id):
    from app.models.Mailgun_Internal import mailgun_send_newsletter
    username = session['username']
    mg_api_private = session['mg_api_private']
    mg_domain = session['mg_domain']
    newsletter = Newsletter.query.filter_by(username=username, id=newsletter_id).first()
    sender = newsletter.sender
    recipients = newsletter.recipients
    subject = newsletter.subject
    message = newsletter.message
    tags = newsletter.tags
    campaign = newsletter.campaign
    response = mailgun_send_newsletter(mg_api_private, mg_domain, sender, recipients, subject, message, tags, campaign)
    return response


def delete_newsletter(newsletter_id):
    username = session['username']
    newsletter = Newsletter.query.filter_by(username=username, id=newsletter_id).first()
    db.session.delete(newsletter)
    return db.session.commit()


def edit_newsletter(newsletter_id):
    username = session['username']
    newsletter_data = Newsletter.query.filter_by(username=username, id=newsletter_id).first()
    return newsletter_data


def update_newsletter_status(mailgun_response, newsletter_id):
    if "Queued. Thank you." in mailgun_response['message']:
        queued = True
    else:
        queued = False

    if queued:
        mg_id = mailgun_response['id']
        newsletter = Newsletter.query.filter_by(id=newsletter_id).first()
        newsletter.mg_status = True
        newsletter.mg_id = mg_id
        return db.session.commit()
