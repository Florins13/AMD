# Exercise 4: Filter Relevant Data for Market-Basket Analysis

## Overview
Reduces data complexity by filtering visitors with 5-30 sessions for market-basket analysis.

## Implementation
Based on PRACTICE_7 `v_export` view, adapted for PROJECT_B requirements.

## SQL Script
- **04_filter_data_exercise4.sql** - Creates filtered view `v_export_filtered`

## Filtering Criteria

### Session Range
- **Minimum sessions**: 5
- **Maximum sessions**: 30
- Rationale: Filters out single-visit users and extremely active users for balanced analysis

### Product Filtering
Excludes invalid product_gui values:
- Navigation categories: `'open'`, `'home'`, `'Spy'`, `'Tecnologia'`, `'Divertimento'`, `'Jogos'`
- System URLs: `'/customer/account/login/'`, `'/customer/account/forgotpassword/'`, `'/customer/account/create/'`
- Generic paths: URLs starting with `/` or `/catalog/`

## Results

### Filtered Dataset Statistics
```
Total filtered events:    19,364
Total filtered visitors:   1,253
Total filtered sessions:   4,945
Total filtered products:   1,768
```

### Comparison with Original Dataset
```
Original:  415,863 events from 263,137 visitors
Filtered:   19,364 events from   1,253 visitors
Reduction:      95.3% of events filtered out
```

### Why This Reduction?
1. **Session filter (5-30)**: Only 1,253 visitors (0.48%) had 5-30 sessions
2. **Product filter**: Removed invalid/navigation entries
3. **Focus**: Analysis on engaged users with meaningful product interactions

## Database View Created

### v_export_filtered
```sql
CREATE VIEW v_export_filtered( cookie_id, session_id, product_gui )
AS
SELECT T1.cookie_id, session_id, product_gui
FROM ( SELECT *
       FROM v_cookie_number_of_sessions
       WHERE number_of_sessions >= 5 AND number_of_sessions <= 30 ) AS T1
     INNER JOIN
     track AS T2
     ON ( T1.cookie_id = T2.cookie_id )
WHERE product_gui NOT IN ( 'open', 'home', ... )
  AND product_gui NOT LIKE '/%'
  AND product_gui NOT LIKE '/catalog/%'
;
```

## How to Run

### Individual Execution
```bash
cd /home/guerra38/ISEL/AMD/2526/AMD/PROJECT_B/scripts
./shell_scripts/_go04.sh
```

### Full Pipeline (Exercises 3 & 4)
```bash
cd /home/guerra38/ISEL/AMD/2526/AMD/PROJECT_B/scripts
python3 _goPy.py
```

## Output Includes
1. Total filtered events
2. Total filtered visitors
3. Total filtered sessions
4. Total filtered products
5. Distribution of sessions (5-30 range)
6. Sample of filtered data (first 20 rows)

## Next Steps
This filtered view (`v_export_filtered`) will be used in:
- **Exercise 5**: Export transactions to file
- **Exercise 6**: Transform to basket format
- **Exercise 7**: Market-basket analysis (association rules)

## Session Distribution (5-30 sessions)
The filtered dataset includes visitors with the following session counts:
- 5 sessions: 692 visitors
- 6 sessions: 559 visitors
- 7 sessions: 403 visitors
- ... continuing up to 30 sessions

This provides a balanced dataset for discovering meaningful product associations without noise from one-time visitors or extremely active outliers.
