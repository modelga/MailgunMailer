import requests
from flask import session


def mailgun_get_groups():
	try:
		from datetime import datetime
		mg_api_private = session['mg_api_private']
		response = requests.get(
			"https://api.mailgun.net/v3/lists",
			auth=("api", mg_api_private),
		)

		recipients = response.json()['items']
		for recipient in recipients:
			created_at = recipient['created_at']
			map_time = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S %z')
			recipient['created_at'] = map_time
		return recipients

	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		print("Problem in getting data for mailgun_get_groups. Using Dummy data.")
		recipients = []
		return recipients


def mailgun_get_group(address):
	try:
		from datetime import datetime
		mg_api_private = session['mg_api_private']
		url = "https://api.mailgun.net/v3/lists/" + address
		# print(url)
		response = requests.get(
			url,
			auth=("api", mg_api_private),
		)
		data = response.json()['list']
		return data

	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		print("Problem in getting data for mailgun_get_group. Using Dummy data.")
		group = []
		return group


def mailgun_create_group(list_address, list_name, list_description):
	mg_api_private = session['mg_api_private']
	url = "https://api.mailgun.net/v3/lists"
	response = requests.post(
		url,
		auth=("api", mg_api_private),
		data={"address": list_address, "name": list_name, "description": list_description},
	)

	data = response.json()
	return data


def mailgun_delete_group(address):
	try:
		from datetime import datetime
		mg_api_private = session['mg_api_private']
		url = "https://api.mailgun.net/v3/lists/" + address
		# print(url)
		response = requests.delete(
			url,
			auth=("api", mg_api_private),
		)
		data = response.json()['list']
		return data

	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		print("Problem in getting data for mailgun_get_groups. Using Dummy data.")
		recipients = []
		return recipients


def mailgun_get_group_members(address):
	try:
		from datetime import datetime
		mg_api_private = session['mg_api_private']
		url = "https://api.mailgun.net/v3/" + "lists/" + address + "/members"
		response = requests.get(
			url,
			auth=("api", mg_api_private),
		)
		data = response.json()['items']
		return data

	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		print("Problem in getting data for mailgun_get_group members. Using Dummy data.")
		recipients = []
		return recipients


def mailgun_api_add_group_member(mg_api_private, address, member_email, ip_addr):
	try:
		from datetime import datetime
		url = "https://api.mailgun.net/v3/" + "lists/" + address + "/members"
		request_vars = '{"ip": "%s"}' % str(ip_addr)
		response = requests.post(
			url,
			auth=("api", mg_api_private),
			data={"upsert": True,
			      "subscribed": True,
			      "address": member_email,
			      "name": "Web Form",
			      "description": "Web Form",
			      "vars": str(request_vars),
			      }
		)
		data = response.json()
		return data

	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		return "Problem"


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

		return campaigns
	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
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


def mailgun_send_newsletter(sender, recipients, subject, message, tags, campaign):
	mg_api_private = session['mg_api_private']
	mg_domain = session['mg_domain']
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
