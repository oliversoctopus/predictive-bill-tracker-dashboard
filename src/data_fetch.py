import requests
import pandas as pd
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
CONGRESS_API_KEY = os.getenv('CONGRESS_API_KEY')
LEGISCAN_API_KEY = os.getenv('LEGISCAN_API_KEY')  # If using

def fetch_bill_titles(bill_id, congress=118, bill_type='hr'):
    """
    Fetch all titles for a bill
    """
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/titles?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        titles_data = data.get('titles', [])
        
        # Find the short title
        short_title = ''
        official_title = ''
        display_title = ''
        
        for title_item in titles_data:
            if isinstance(title_item, dict):
                title_type = title_item.get('titleType', '').lower()
                title_text = title_item.get('title', '')
                
                if 'short' in title_type and title_text and not short_title:
                    short_title = title_text
                elif 'official' in title_type and title_text:
                    official_title = title_text
                elif 'display' in title_type and title_text:
                    display_title = title_text
        
        return {
            'short_title': short_title,
            'official_title': official_title,
            'display_title': display_title
        }
    else:
        return {'short_title': '', 'official_title': '', 'display_title': ''}

def fetch_bill(bill_id, congress=118, bill_type='hr'):
    """
    Fetch comprehensive bill information including sponsors, committees, and subjects
    """
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        bill_data = data.get('bill', {})
        
        # Extract sponsor information - handle list or single sponsor
        sponsors_data = bill_data.get('sponsors', [])
        if isinstance(sponsors_data, dict):
            sponsors_data = [sponsors_data]
        elif not isinstance(sponsors_data, list):
            sponsors_data = []
            
        sponsor_names = [s.get('fullName', '') for s in sponsors_data if isinstance(s, dict)]
        sponsor_parties = [s.get('party', 'Unknown') for s in sponsors_data if isinstance(s, dict)]
        sponsor_states = [s.get('state', 'Unknown') for s in sponsors_data if isinstance(s, dict)]
        
        # Count Democrats and Republicans
        dem_sponsors = sum(1 for p in sponsor_parties if p == 'D')
        rep_sponsors = sum(1 for p in sponsor_parties if p == 'R')
        
        # Extract committee information - handle various structures
        committees = bill_data.get('committees', {})
        committee_names = []
        
        if isinstance(committees, dict):
            items = committees.get('item', [])
            if isinstance(items, list):
                committee_names = [c.get('name', '') for c in items if isinstance(c, dict) and c.get('name')]
            elif isinstance(items, dict) and items.get('name'):
                committee_names = [items.get('name')]
        elif isinstance(committees, list):
            committee_names = [c.get('name', '') for c in committees if isinstance(c, dict) and c.get('name')]
        
        # Extract policy area - handle different structures
        policy_area_data = bill_data.get('policyArea', {})
        if isinstance(policy_area_data, dict):
            policy_area = policy_area_data.get('name', 'Unknown')
        elif isinstance(policy_area_data, str):
            policy_area = policy_area_data
        else:
            policy_area = 'Unknown'
        
        # Extract cosponsors count
        cosponsors = bill_data.get('cosponsors', {})
        if isinstance(cosponsors, dict):
            cosponsor_count = cosponsors.get('count', 0)
        elif isinstance(cosponsors, int):
            cosponsor_count = cosponsors
        else:
            cosponsor_count = 0
        
        # Extract latest action
        latest_action = bill_data.get('latestAction', {})
        if not isinstance(latest_action, dict):
            latest_action = {}
        
        # Extract title information
        title = bill_data.get('title', '')
        
        # Create DataFrame with comprehensive information first
        df = pd.DataFrame({
            'bill_id': [f"{congress}-{bill_type.upper()}-{bill_id}"],
            'title': [title],
            'short_title': [''],  # Will be filled by separate API call
            'status': [latest_action.get('text', '')],
            'action_date': [latest_action.get('actionDate', '')],
            'sponsors': [', '.join(sponsor_names)],
            'sponsor_parties': [', '.join(sponsor_parties) if sponsor_parties else 'Unknown'],
            'sponsor_states': [', '.join(sponsor_states)],
            'dem_sponsors': [dem_sponsors],
            'rep_sponsors': [rep_sponsors],
            'cosponsor_count': [cosponsor_count],
            'committees': [', '.join(committee_names)],
            'policy_area': [policy_area],
            'introduced_date': [bill_data.get('introducedDate', '')],
            'congress': [bill_data.get('congress', congress)],
            'type': [bill_data.get('type', bill_type.upper())],
            'is_bipartisan': [dem_sponsors > 0 and rep_sponsors > 0]
        })
        
        # Fetch titles separately
        titles_info = fetch_bill_titles(bill_id, congress, bill_type)
        if titles_info['short_title']:
            df.loc[0, 'short_title'] = titles_info['short_title']
        elif titles_info['display_title']:
            df.loc[0, 'short_title'] = titles_info['display_title']
        
        return df
    else:
        print(f"Error for bill {bill_id}: {response.status_code}")
        return pd.DataFrame()

def fetch_bill_actions(bill_id, congress=118, bill_type='hr'):
    """
    Fetch bill actions with more detail
    """
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/actions?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        actions_data = data.get('actions', [])
        
        actions = []
        for a in actions_data:
            # Handle committees field which can be a dict or list
            committees_data = a.get('committees', {})
            
            # Extract committee names based on data structure
            if isinstance(committees_data, dict):
                # If it's a dict, look for 'item' field
                items = committees_data.get('item', [])
                if isinstance(items, list):
                    committee_names = [c.get('name', '') for c in items if isinstance(c, dict)]
                elif isinstance(items, dict):
                    committee_names = [items.get('name', '')]
                else:
                    committee_names = []
            elif isinstance(committees_data, list):
                # If it's already a list of committees
                committee_names = [c.get('name', '') for c in committees_data if isinstance(c, dict)]
            else:
                committee_names = []
            
            action = {
                'bill_id': bill_id,
                'date': a.get('actionDate'),
                'text': a.get('text'),
                'type': a.get('type'),
                'action_code': a.get('actionCode'),
                'source_system': a.get('sourceSystem', {}).get('name', ''),
                'committees': ', '.join(committee_names)
            }
            actions.append(action)
        
        df_actions = pd.DataFrame(actions)
        return df_actions
    else:
        print(f"Error for actions {bill_id}: {response.status_code}")
        return pd.DataFrame()

def fetch_cosponsors(bill_id, congress=118, bill_type='hr'):
    """
    Fetch detailed cosponsor information
    """
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/cosponsors?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        cosponsors_data = data.get('cosponsors', [])
        
        # Handle case where cosponsors is a dict with items
        if isinstance(cosponsors_data, dict):
            items = cosponsors_data.get('item', [])
            if isinstance(items, list):
                cosponsors_data = items
            elif isinstance(items, dict):
                cosponsors_data = [items]
            else:
                cosponsors_data = []
        elif not isinstance(cosponsors_data, list):
            cosponsors_data = []
        
        cosponsors = []
        for c in cosponsors_data:
            if isinstance(c, dict):
                cosponsor = {
                    'bill_id': f"{congress}-{bill_type.upper()}-{bill_id}",
                    'name': c.get('fullName', ''),
                    'party': c.get('party', ''),
                    'state': c.get('state', ''),
                    'district': c.get('district', ''),
                    'sponsored_date': c.get('sponsorshipDate', ''),
                    'is_original': c.get('isOriginalCosponsor', False)
                }
                cosponsors.append(cosponsor)
        
        df_cosponsors = pd.DataFrame(cosponsors)
        
        # Calculate party breakdown
        if not df_cosponsors.empty:
            party_counts = df_cosponsors['party'].value_counts().to_dict()
            return df_cosponsors, party_counts
        else:
            return df_cosponsors, {}
    else:
        print(f"Error for cosponsors {bill_id}: {response.status_code}")
        return pd.DataFrame(), {}

def fetch_subjects(bill_id, congress=118, bill_type='hr'):
    """
    Fetch bill subjects
    """
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/subjects?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        subjects = data.get('subjects', {})
        
        # Extract legislative subjects - handle different structures
        legislative_subjects = subjects.get('legislativeSubjects', [])
        
        # Handle case where legislativeSubjects is a list directly
        if isinstance(legislative_subjects, list):
            subject_names = [s.get('name', '') for s in legislative_subjects if isinstance(s, dict) and s.get('name')]
        # Handle case where it's a dict with 'item' field
        elif isinstance(legislative_subjects, dict):
            items = legislative_subjects.get('item', [])
            if isinstance(items, list):
                subject_names = [s.get('name', '') for s in items if isinstance(s, dict) and s.get('name')]
            elif isinstance(items, dict) and items.get('name'):
                subject_names = [items.get('name', '')]
            else:
                subject_names = []
        else:
            subject_names = []
        
        # Extract policy area - handle different structures
        policy_area = subjects.get('policyArea', {})
        if isinstance(policy_area, dict):
            policy_area_name = policy_area.get('name', 'Unknown')
        elif isinstance(policy_area, str):
            policy_area_name = policy_area
        else:
            policy_area_name = 'Unknown'
        
        return {
            'subjects': subject_names,
            'policy_area': policy_area_name,
            'subject_count': len(subject_names)
        }
    else:
        print(f"Error for subjects {bill_id}: {response.status_code}")
        return {'subjects': [], 'policy_area': 'Unknown', 'subject_count': 0}

def fetch_text_versions(bill_id, congress=118, bill_type='hr'):
    """
    Fetch available text versions of the bill
    """
    url = f'https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_id}/text?api_key={CONGRESS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        text_versions_data = data.get('textVersions', [])
        
        # Handle case where textVersions is a dict with items
        if isinstance(text_versions_data, dict):
            items = text_versions_data.get('item', [])
            if isinstance(items, list):
                text_versions_data = items
            elif isinstance(items, dict):
                text_versions_data = [items]
            else:
                text_versions_data = []
        elif not isinstance(text_versions_data, list):
            text_versions_data = []
        
        versions = []
        for v in text_versions_data:
            if isinstance(v, dict):
                formats_data = v.get('formats', [])
                format_types = []
                
                if isinstance(formats_data, list):
                    format_types = [f.get('type', '') for f in formats_data if isinstance(f, dict)]
                elif isinstance(formats_data, dict):
                    format_types = [formats_data.get('type', '')]
                
                version = {
                    'type': v.get('type', ''),
                    'date': v.get('date', ''),
                    'formats': format_types
                }
                versions.append(version)
        
        return pd.DataFrame(versions)
    else:
        print(f"Error for text versions {bill_id}: {response.status_code}")
        return pd.DataFrame()

def fetch_public_comments(docket_id='CMS-2024-0001'):
    """
    Fetch public comments (unchanged from original)
    """
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

def fetch_comprehensive_bill_data(bill_id, congress=118, bill_type='hr'):
    """
    Fetch all available data for a bill
    """
    # Get basic bill info
    bill_df = fetch_bill(bill_id, congress, bill_type)
    
    if bill_df.empty:
        return None
    
    # Get additional data
    actions_df = fetch_bill_actions(bill_id, congress, bill_type)
    cosponsors_df, party_breakdown = fetch_cosponsors(bill_id, congress, bill_type)
    subjects_data = fetch_subjects(bill_id, congress, bill_type)
    text_versions_df = fetch_text_versions(bill_id, congress, bill_type)
    
    # Calculate original cosponsor count
    original_cosponsor_count = 0
    if not cosponsors_df.empty and 'is_original' in cosponsors_df.columns:
        original_cosponsor_count = cosponsors_df['is_original'].sum()
    
    # Compile comprehensive data
    comprehensive_data = {
        'bill_info': bill_df,
        'actions': actions_df,
        'cosponsors': cosponsors_df,
        'cosponsor_party_breakdown': party_breakdown,
        'subjects': subjects_data,
        'text_versions': text_versions_df,
        'metrics': {
            'total_actions': len(actions_df),
            'total_cosponsors': len(cosponsors_df),
            'original_cosponsor_count': original_cosponsor_count,
            'dem_cosponsors': party_breakdown.get('D', 0),
            'rep_cosponsors': party_breakdown.get('R', 0),
            'ind_cosponsors': party_breakdown.get('I', 0),
            'bipartisan_score': calculate_bipartisan_score(bill_df, party_breakdown),
            'days_since_introduction': calculate_days_active(bill_df),
            'committee_count': len(bill_df['committees'].values[0].split(',')) if bill_df['committees'].values[0] else 0,
            'dem_sponsors': bill_df['dem_sponsors'].values[0] if not bill_df.empty else 0,
            'rep_sponsors': bill_df['rep_sponsors'].values[0] if not bill_df.empty else 0,
            'total_sponsors': (bill_df['dem_sponsors'].values[0] + bill_df['rep_sponsors'].values[0]) if not bill_df.empty else 1,
            'dem_total': bill_df['dem_sponsors'].values[0] + party_breakdown.get('D', 0) if not bill_df.empty else 0,
            'rep_total': bill_df['rep_sponsors'].values[0] + party_breakdown.get('R', 0) if not bill_df.empty else 0,
            'party_dominance': abs((bill_df['dem_sponsors'].values[0] + party_breakdown.get('D', 0)) - 
                                 (bill_df['rep_sponsors'].values[0] + party_breakdown.get('R', 0))) / 
                              max((bill_df['dem_sponsors'].values[0] + bill_df['rep_sponsors'].values[0] + 
                                   len(cosponsors_df)), 1) if not bill_df.empty else 0
        }
    }
    
    return comprehensive_data

def calculate_bipartisan_score(bill_df, party_breakdown):
    """
    Calculate a bipartisan score based on sponsor and cosponsor party distribution
    """
    total_d = bill_df['dem_sponsors'].values[0] + party_breakdown.get('D', 0)
    total_r = bill_df['rep_sponsors'].values[0] + party_breakdown.get('R', 0)
    total = total_d + total_r
    
    if total == 0:
        return 0
    
    # Score is higher when party distribution is more even
    minority_party = min(total_d, total_r)
    bipartisan_score = (minority_party / total) * 2  # Max score of 1.0 when 50/50
    
    return bipartisan_score

def calculate_days_active(bill_df):
    """
    Calculate days since bill introduction
    """
    from datetime import datetime
    
    introduced_date = bill_df['introduced_date'].values[0]
    if introduced_date:
        try:
            intro_date = pd.to_datetime(introduced_date)
            days_active = (datetime.now() - intro_date).days
            return days_active
        except:
            return 0
    return 0

# Only run this part if the script is executed directly (not imported)
if __name__ == "__main__":
    # Fetch multiple bills
    bill_ids = list(range(1, 51)) + [f'S{i}' for i in range(1, 21)]  # H.R.1-50, S.1-20
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