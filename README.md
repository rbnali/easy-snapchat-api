# easy-snapchat-api
Get your daily Snapchat marketing spendings using the API

# Requirements

Please install all the necesssary requirements with the following command:
```
pip install -r requirements.txt
```

You will also need to add your snapchat credentials as environment variables.

```
export SNAPCHAT_CLIENT_ID=YOUR_CLIENT_ID
export SNAPCHAT_CLIENT_SECRET=YOUR_CLIENT_SECRET
export SNAPCHAT_REFRESH_TOKEN=YOUR_REFRESH_TOKEN
export SNAPCHAT_ORGANIZATION_ID=YOUR_ORGANIZATION_ID
export SNAPCHAT_AD_ACCOUNTS_ID=YOUR_AD_ACCOUNTS_ID
}
```

If you don't have Snapchat API credentials, please have a look to https://github.com/rbnali/easy-snapchat-accesstoken

# Arguments

Arguments       | Help
-------------   | -------------
-start          | Start date of the report in the following format: YYYY-mm-dd
-end            | End date of the report in the following format: YYYY-mm-dd

The time difference between the start and end date must be lower than 30 days due to Snapchat API rate limits. If you need data for more than 30 days, you can easily adapt that script and iterate requests.

# Example

```
python snapchat.py -start 2019-08-01 -end 2019-08-30
```

# Output description

CSV file called `snap.csv` with the following columns:

Column                        | Description
-------------                 | -------------
campaign_id                   | Your Snapchat campaign ID
start_time                    | Begining of the period
end_time                      | End of the period
impressions                   | Impressions of your campaign ads
spends                        | Spendings in USD
