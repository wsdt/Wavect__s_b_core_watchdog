import urllib.request, json, requests
import time

# GET #
api_base_url = "https://api.dev.wavect.io/api/"
api_version = "v1/"
api_type = "mobile/"
api_test_interval_in_seconds = 60 * 60 # 1 hour
starttime = time.time()

# Only add routes which have no persisting effect on the database (e.g. queries)
api_uris_to_test = [
	"challenge/current"
]

# POST #
slack_webhook = "https://hooks.slack.com/services/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"
post_headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}


def send_msg_to_slack(res, err, full_api_uri):
	msg = '{"text": "*An error occurred in your api.*\nApi-Version: *'+api_version+'*\n' \
	'Api-Url: *'+full_api_uri+'*\n' \
	'Reported Errors: `'+json.dumps(err).replace('"', '\\"')+'`\n' \
	'Returned Result: `'+json.dumps(res).replace('"', '\\"')+'`"}'
	r = requests.post(slack_webhook, data=msg, headers=post_headers)
	

def evaluate_route(api_uri):
	full_api_uri = api_base_url+api_type+api_version+api_uri
	with urllib.request.urlopen(full_api_uri) as url:
		data = json.loads(url.read().decode())
		if data is None or data["err"] is not None or data["res"] is None:  # is res none for a test-query then we assume sth. is wrong
			send_msg_to_slack(data["res"], data["err"], full_api_uri)
		

def evaluate_all_routes():
	# Main TODO TRIGGER in interval via docker 
	for api_uri in api_uris_to_test:
		evaluate_route(api_uri)
	

while True:
		print("Evaluating routes at "+time.ctime())
		time.sleep(api_test_interval_in_seconds - ((time.time() - starttime) % 60.0))