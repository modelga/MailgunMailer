import requests
from flask import session


def mailgun_get_groups():
	try:
		mg_api_private = session['mg_api_private']
		response = requests.get(
			"https://api.mailgun.net/v3/lists",
			auth=("api", mg_api_private),
		)

		data = response.json()['items']

		recipients = []

		for recipient in data:
			recipients.append(recipient['address'])

		return recipients
	except:
		print("Problem in getting data for mailgun_get_groups. Using Dummy data.")
		recipients = []
		return recipients


def mailgun_get_campaigns():
	try:
		mg_api_private = session['mg_api_private']
		mg_domain = session['mg_domain']
		response = requests.get(
			"https://api.mailgun.net/v3/" + mg_domain + "/campaigns",
			auth=("api", mg_api_private),
		)

		data = response.json()['items']

		campaigns = []
		for campaign in data:
			campaigns.append(campaign['name'])

		# print("CAMP:", campaigns)
		return campaigns
	except:
		print("Problem in getting data for mailgun_get_campaigns. Using Dummy data.")
		campaigns = []
		return campaigns


def mailgun_add_campaigns(campaign_name):
	mg_api_private = session['mg_api_private']
	mg_domain = session['mg_domain']
	response = requests.post(
		"https://api.mailgun.net/v3/" + mg_domain + "/campaigns",
		auth=("api", mg_api_private),
		data={"name": campaign_name,
		      "id": campaign_name},
	)

	data = response.json()
	return data


def mailgun_delete_campaigns(campaign_name):
	mg_api_private = session['mg_api_private']
	mg_domain = session['mg_domain']
	response = requests.delete(
		"https://api.mailgun.net/v3/" + mg_domain + "/campaigns/" + campaign_name,
		auth=("api", mg_api_private)
	)

	data = response.json()
	return data


def mailgun_send_newsletter(mg_api_private, mg_domain, sender, recipients, subject, message, tags, campaign):
	url = "https://api.mailgun.net/v3/" + str(mg_domain) + "/messages"
	response = requests.post(
		url,
		auth=("api", mg_api_private),
		data={"from": sender,
		      "to": recipients,
		      "subject": subject,
		      "html": message,
		      "o:tag": tags,
		      "o:campaign": campaign
		      }
	)

	return response.json()
