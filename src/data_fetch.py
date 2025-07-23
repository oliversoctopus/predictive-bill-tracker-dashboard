import requests
import pandas as pd
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
CONGRESS_API_KEY = os.getenv('CONGRESS_API_KEY')
LEGISCAN_API_KEY = os.getenv('LEGISCAN_API_KEY')  # If using

def fetch_bill(bill_id, congress=118, bill_type='hr'):
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame({
            'bill_id': [bill_id],
            'title': [data.get('bill', {}).get('title')],
            'status': [data.get('bill', {}).get('latestAction', {}).get('text')],
            'sponsors': [', '.join([s['fullName'] for s in data.get('bill', {}).get('sponsors', [])])]
        })
        return df
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_bill_actions(bill_id, congress=118, bill_type='hr'):
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/actions?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        actions = [{'date': a.get('actionDate'), 'text': a.get('text')} for a in data.get('actions', [])]
        df_actions = pd.DataFrame(actions)
        return df_actions
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_public_comments(docket_id='CMS-2025-0001'):
    url = f'https://api.regulations.gov/v4/comments?filter[docketId]={docket_id}&api_key=DEMO_KEY'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        comments = [item['attributes']['comment'] for item in data.get('data', []) if 'comment' in item['attributes']]
        df_comments = pd.DataFrame({'comment': comments})
        return df_comments
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
bill_data = fetch_bill(1234)
if bill_data is not None:
    bill_data.to_csv('data/sample_bill.csv', index=False)

actions_data = fetch_bill_actions(1234)
if actions_data is not None:
    actions_data.to_csv('data/bill_actions.csv', index=False)

comments_data = fetch_public_comments()
if comments_data is not None:
    comments_data.to_csv('data/public_comments.csv', index=False)

# Store in SQLite
conn = sqlite3.connect('data/bills.db')
if bill_data is not None:
    bill_data.to_sql('bills', conn, if_exists='append')
if actions_data is not None:
    actions_data.to_sql('actions', conn, if_exists='append')
if comments_data is not None:
    comments_data.to_sql('comments', conn, if_exists='append')
conn.close()

import schedule
import time

def job():
    print("Fetching updates...")
    fetch_bill(1234)
    fetch_bill_actions(1234)
    fetch_public_comments()

schedule.every(15).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)