# Data Documentation

## Data Sources
- **Primary Source**: Congress.gov API (v3) – Official U.S. Congress data.
  - Endpoints: `/bill/{congress}/{bill_type}`, `/bill/{congress}/{bill_type}/{bill_id}` (details like sponsors, actions, committees).
  - API Key: Required (stored in .env); rate-limited.
- **Scope**: 118th Congress (2023-2025); all HR, S, HJRES, SJRES bills (~6,000 raw, ~16,500 post-processing).
- **Ethical Note**: Public domain data; no scraping—API compliant. No personal data beyond public sponsor info.

## Data Acquisition
- Notebook: `data/extract_118th_congress.ipynb`
  - Fetches bills in batches (limit=250).
  - Handles retries, caching in `118th_congress_cache/`.
  - Extracts: Bill ID, title, sponsors/cosponsors, actions, committees, subjects, timelines.
- Checkpointing: Resumes if interrupted.

## Preprocessing
- Notebook: `data/combine_and_preprocess.ipynb`
  - Combines House/Senate CSVs.
  - Identifies failures: Since 118th ended (Jan 2025), all non-passed = failed.
    - Reasons: Died in committee (87%), stalled (8%), etc.
  - Features: Party balances, bipartisan scores, activity rates.
  - Outcomes: Passed (1), Failed (0); 'Viable' target for traction.
- Saved Files:
  - `bills_118th_congress_full.csv`: All bills (~6K rows, 30+ columns).
  - `bills_118th_congress_training_enhanced.csv`: With outcomes (~16K rows; expanded for failures).
- Preprocessing Steps: Date parsing, missing value fills (e.g., cosponsors=0), encoding (party/policy), derived features (e.g., days_active).

## Data Structure
- Columns (key ones): bill_id, title, sponsor_party, cosponsor_count, action_count, committee_count, passed, viable.
- Size: CSVs ~10-20MB each.
- Privacy: No sensitive data; aggregated sponsor stats only.

For usage: Load via pandas in app/model scripts.