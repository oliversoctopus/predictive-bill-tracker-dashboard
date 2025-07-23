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
        print(f"Error for bill {bill_id}: {response.status_code}")
        return pd.DataFrame()

def fetch_bill_actions(bill_id, congress=118, bill_type='hr'):
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/actions?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        actions = [{'bill_id': bill_id, 'date': a.get('actionDate'), 'text': a.get('text')} for a in data.get('actions', [])]
        df_actions = pd.DataFrame(actions)
        return df_actions
    else:
        print(f"Error for actions {bill_id}: {response.status_code}")
        return pd.DataFrame()

def fetch_public_comments(docket_id='CMS-2024-0001'):
    url = f'https://api.regulations.gov/v4/comments?filter[docketId]={docket_id}&api_key=DEMO_KEY'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        comments = [item['attributes']['comment'] for item in data.get('data', []) if 'comment' in item['attributes']]
        df_comments = pd.DataFrame({'comment': comments})
        return df_comments
    else:
        print(f"Error for docket {docket_id}: {response.status_code}")
        return pd.DataFrame()

# Fetch multiple bills
bill_ids = [1, 23, 82, 139, 670, 2474, 2701, 3086, 5009, 8070, 8281, 8998, 9495, 10065, 10515, 10545]  # From Congress.gov
bill_dfs = []
actions_dfs = []
for bid in bill_ids:
    bill_df = fetch_bill(bid)
    if not bill_df.empty:
        bill_dfs.append(bill_df)
    actions_df = fetch_bill_actions(bid)
    if not actions_df.empty:
        actions_dfs.append(actions_df)

all_bills = pd.concat(bill_dfs, ignore_index=True)
all_actions = pd.concat(actions_dfs, ignore_index=True)
comments_data = fetch_public_comments()

# Save with UTF-8
all_bills.to_csv('data/sample_bill.csv', index=False, encoding='utf-8')
all_actions.to_csv('data/bill_actions.csv', index=False, encoding='utf-8')
if not comments_data.empty:
    comments_data.to_csv('data/public_comments.csv', index=False, encoding='utf-8')
else:
    pd.DataFrame({'comment': ['No comments found']}).to_csv('data/public_comments.csv', index=False, encoding='utf-8')

# Store in SQLite
conn = sqlite3.connect('data/bills.db')
all_bills.to_sql('bills', conn, if_exists='append')
all_actions.to_sql('actions', conn, if_exists='append')
comments_data.to_sql('comments', conn, if_exists='append')
conn.close()