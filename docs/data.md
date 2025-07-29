\# Data Documentation



\## Data Sources

\- \*\*Primary Source\*\*: Congress.gov API (v3) – Official U.S. Congress data.

&nbsp; - Endpoints: `/bill/{congress}/{bill\_type}`, `/bill/{congress}/{bill\_type}/{bill\_id}` (details like sponsors, actions, committees).

&nbsp; - API Key: Required (stored in .env); rate-limited.

\- \*\*Scope\*\*: 118th Congress (2023-2025); all HR, S, HJRES, SJRES bills (~6,000 raw, ~16,500 post-processing).

\- \*\*Ethical Note\*\*: Public domain data; no scraping—API compliant. No personal data beyond public sponsor info.



\## Data Acquisition

\- Notebook: `data/extract\_118th\_congress.ipynb`

&nbsp; - Fetches bills in batches (limit=250).

&nbsp; - Handles retries, caching in `118th\_congress\_cache/`.

&nbsp; - Extracts: Bill ID, title, sponsors/cosponsors, actions, committees, subjects, timelines.

\- Checkpointing: Resumes if interrupted.



\## Preprocessing

\- Notebook: `data/combine\_and\_preprocess.ipynb`

&nbsp; - Combines House/Senate CSVs.

&nbsp; - Identifies failures: Since 118th ended (Jan 2025), all non-passed = failed.

&nbsp;   - Reasons: Died in committee (87%), stalled (8%), etc.

&nbsp; - Features: Party balances, bipartisan scores, activity rates.

&nbsp; - Outcomes: Passed (1), Failed (0); 'Viable' target for traction.

\- Saved Files:

&nbsp; - `bills\_118th\_congress\_full.csv`: All bills (~6K rows, 30+ columns).

&nbsp; - `bills\_118th\_congress\_training\_enhanced.csv`: With outcomes (~16K rows; expanded for failures).

\- Preprocessing Steps: Date parsing, missing value fills (e.g., cosponsors=0), encoding (party/policy), derived features (e.g., days\_active).



\## Data Structure

\- Columns (key ones): bill\_id, title, sponsor\_party, cosponsor\_count, action\_count, committee\_count, passed, viable.

\- Size: CSVs ~10-20MB each.

\- Privacy: No sensitive data; aggregated sponsor stats only.



For usage: Load via pandas in app/model scripts.

