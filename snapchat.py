### REQUIREMENTS ###
import json
import pytz
from datetime import datetime, timedelta, timezone
import requests
import pandas as pd
import argparse


### GENERAL ###
def day_diff_strptime(start, end):
	s = datetime.strptime(start, '%Y-%m-%d')
	e = datetime.strptime(end, '%Y-%m-%d')
	return (e-s).days


### SNAPCHAT ###
def get_snapchat_access_token(snap_credentials):

	# Initialize
	access_url = 'https://accounts.snapchat.com/login/oauth2/access_token'
	access_params = {
		'client_id': snap_credentials['client_id'],
		'client_secret': snap_credentials['client_secret'],
		'code': snap_credentials['refresh_token'],
		'grant_type': 'refresh_token',
	}

	# Get
	res = requests.post(
		access_url,
		params = access_params
	)

	return res.json()['access_token']


def get_all_campaigns(access_token, ad_accounts_id):
	# Initialize
	url_campaigns = 'https://adsapi.snapchat.com/v1/adaccounts/%s/campaigns' % (ad_accounts_id)
	headers= {'Authorization': 'Bearer %s' % (access_token)}

	# Get
	res= requests.get(
		url_campaigns,
		headers = headers
	)

	# Store
	campaign_ids = list()
	for c in res.json()['campaigns']:
		campaign_ids += [c['campaign']['id']]

	return campaign_ids


def get_report_from_campaign_id(access_token, campaign_id, start_date, end_date):  
	# Initialize
	headers= {'Authorization': 'Bearer %s' % (access_token)}
	
	# Get dates
	start_time = (pytz
		.timezone('Europe/Paris')
		.localize(datetime.strptime(start_date, '%Y-%m-%d'))
		.isoformat()
	)
	end_time = (pytz
		.timezone('Europe/Paris')
		.localize(datetime.strptime(end_date, '%Y-%m-%d'))
		.isoformat()
	)
	
	# Prepare
	df = pd.DataFrame()
	url_reporting = 'https://adsapi.snapchat.com/v1/campaigns/%s/stats' % campaign_id
	params = {
		'start_time':start_time,
		'end_time':end_time,
		'granularity': 'DAY',
	}
	
	# Run
	res= requests.get(
		url_reporting,
		params = params,
		headers = headers
	)

	# Format
	for item in res.json()['timeseries_stats'][0]['timeseries_stat']['timeseries']:
		dict_ = {
			'campaign_id': campaign_id,
			'start_time': item['start_time'],
			'end_time': item['end_time'],
			'impressions': item['stats']['impressions'],
			'spend': item['stats']['spend'] / 1000000
		}
		df = df.append(dict_, ignore_index=True)
	
	return df


### PROCESS ###
def main(snap_credentials, start_date, end_date):
	# Initialize
	snap = pd.DataFrame()

	# Get access token from refresh token
	access_token = get_snapchat_access_token(snap_credentials)

	# Get all campaign ids
	print('Getting Snapchat API access token...')
	campaign_ids = get_all_campaigns(access_token, snap_credentials['ad_accounts_id'])

	# Get campaign data from snapchat API
	print('Getting all campaigns from Snapchat API...')
	for campaign_id in campaign_ids:
		new = get_report_from_campaign_id(
			access_token,
			campaign_id,
			start_date,
			end_date
		)
		snap = pd.concat([snap,new])

	# Send to CSV
	print('Saving data to csv file...')
	snap.to_csv('snap.csv', index=False)


### RUN ###
if __name__ == '__main__':
    # Get snapchat credentials and refresh token
    with open('snap_credentials.json') as f:
        snap_credentials = json.load(f)

    # Parsing args
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', action='store', dest='start', type=str, help='Start date of the report in the following format: YYYY-mm-dd')
    parser.add_argument('-end', action='store', dest='end', type=str, help='End date of the report in the following format: YYYY-mm-dd')
    args = parser.parse_args()

    # Run
    if day_diff_strptime(args.start, args.end) < 31:
    	main(snap_credentials, args.start, args.end)
    else:
    	raise Exception('The difference between start and end date must be less than 30 days')
