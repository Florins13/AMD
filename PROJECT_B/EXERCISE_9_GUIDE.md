# EXERCISE 9 - PIPELINE AUTOMATION

## Overview

Exercise 9 provides **full automation** of the market-basket analysis pipeline, executing Exercises 4-7 sequentially with a single command.

---

## What Gets Automated

The pipeline automates these steps:

1. **Exercise 4:** Filter Data (5-30 sessions)
2. **Exercise 5:** Export Transactions to CSV
3. **Exercise 6:** Transform to Basket Format (normalize + generate .basket/.tab)
4. **Exercise 7:** Association Rules Analysis (explore support/confidence space)

---

## Quick Start

### Run Full Pipeline (Default: maxR=30)

```bash
cd /home/guerra38/ISEL/AMD/2526/AMD/PROJECT_B/scripts
python3 exercise9_automate_pipeline.py
```

### Run with Custom maxR

```bash
python3 exercise9_automate_pipeline.py --maxR 50
```

### Skip Specific Steps (if already completed)

```bash
# Skip exercises 4 and 5 (already have filtered data)
python3 exercise9_automate_pipeline.py --skip 4 5

# Skip exercise 6 (already have basket files)
python3 exercise9_automate_pipeline.py --maxR 20 --skip 6
```

### Using Shell Wrapper

```bash
./run_pipeline.sh --maxR 30
```

---

## Command-Line Options

```
usage: exercise9_automate_pipeline.py [-h] [--maxR MAXR] [--skip EXERCISE [...]] [--version]

Options:
  --maxR MAXR        Maximum number of rules for Exercise 7 (default: 30)
  --skip EXERCISE    Skip specific exercises: 4, 5, 6, 7 (space-separated)
  --version          Show version
  -h, --help         Show help message
```

---

## Usage Examples

### Example 1: Complete Fresh Run

```bash
# Run entire pipeline from scratch
python3 exercise9_automate_pipeline.py --maxR 30

# Expected output:
#   - transactions_filtered.txt (1.3 MB)
#   - transactions_basket.basket (535 KB)
#   - transactions_basket.tab (17 MB)
#   - exercise7_results_maxR30.txt (11 KB)
```

### Example 2: Re-run Analysis with Different maxR

```bash
# Already have data, just re-run analysis with maxR=50
python3 exercise9_automate_pipeline.py --maxR 50 --skip 4 5 6

# Only Exercise 7 runs, generates new results file
```

### Example 3: Quick Basket Regeneration

```bash
# Re-generate basket files and re-run analysis
python3 exercise9_automate_pipeline.py --skip 4 5

# Exercises 6 and 7 run
```

---

## Pipeline Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXERCISE 9 PIPELINE                          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Prerequisites Check  │
                    │ - PostgreSQL         │
                    │ - Python 3           │
                    │ - Orange3            │
                    │ - Database access    │
                    │ - Script files       │
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Exercise 4 (SQL)    │
                    │  Filter Data         │
                    │  Output: v_export_   │
                    │          filtered    │
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Exercise 5 (SQL)    │
                    │  Export Transactions │
                    │  Output: transactions│
                    │          _filtered.txt│
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Exercise 6 (Python) │
                    │  Transform to Basket │
                    │  Output: .basket +   │
                    │          .tab files  │
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Exercise 7 (Python) │
                    │  Association Rules   │
                    │  Output: results_    │
                    │          maxR{n}.txt │
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Summary Report     │
                    │   - Execution time   │
                    │   - File sizes       │
                    │   - Success/failures │
                    └──────────────────────┘
```

---

## Prerequisites Check

The script automatically verifies:

- ✅ PostgreSQL installed and accessible
- ✅ Python 3.x available
- ✅ Orange3 library installed (`pip install Orange3`)
- ✅ Database `db_project_b` exists and is accessible
- ✅ All required SQL scripts present
- ✅ All required Python scripts present

If any prerequisite fails, the pipeline stops with a clear error message.

---

## Expected Output Files

After successful execution:

| File | Size | Description |
|------|------|-------------|
| `transactions_filtered.txt` | ~1.3 MB | Filtered transactions (5-30 sessions) |
| `transactions_basket.basket` | ~535 KB | Orange basket format |
| `transactions_basket.tab` | ~17 MB | Orange tab format (matrix) |
| `exercise7_results_maxR{N}.txt` | ~11 KB | Association rules results |

---

## Execution Time

Typical execution times on standard hardware:

- **Exercise 4 (SQL):** 2-3 seconds
- **Exercise 5 (SQL):** 2-3 seconds
- **Exercise 6 (Python):** 1-2 seconds
- **Exercise 7 (Python):** 1-5 seconds (depends on maxR)

**Total Pipeline:** 6-13 seconds for complete run

---

## Error Handling

The pipeline includes comprehensive error handling:

### Automatic Checks
- File existence verification
- Output file size validation
- Command exit code checking
- Timeout protection (60s for SQL, 300s for Python)

### Failure Behavior
- Pipeline stops immediately on any step failure
- Clear error messages with troubleshooting hints
- Exit codes: 0 (success), 1 (failure), 130 (user interrupt)

### Common Issues

#### Issue: "Database 'db_project_b' not accessible"
**Solution:**
```bash
# Check database exists
psql -l | grep db_project_b

# Re-run Exercise 3 if needed
cd scripts
psql -f 00_create_database.sql
psql -d db_project_b -f 01_create_schema.sql
psql -d db_project_b -f 02_import_data.sql
```

#### Issue: "Orange3 not available"
**Solution:**
```bash
pip install Orange3 Orange3-Associate
```

#### Issue: "transactions_filtered.txt not found"
**Solution:**
```bash
# Run exercises 4 and 5 first (don't skip them)
python3 exercise9_automate_pipeline.py
```

---

## Advanced Usage

### Integration with Cron

Automate daily/weekly analysis:

```bash
# Edit crontab
crontab -e

# Run pipeline daily at 2 AM
0 2 * * * cd /home/guerra38/ISEL/AMD/2526/AMD/PROJECT_B/scripts && python3 exercise9_automate_pipeline.py --maxR 30 >> /tmp/pipeline.log 2>&1
```

### Batch Processing Multiple maxR Values

```bash
#!/bin/bash
# Run analysis with different maxR values

for maxR in 10 20 30 40 50; do
    echo "Running pipeline with maxR=$maxR"
    python3 exercise9_automate_pipeline.py --maxR $maxR --skip 4 5 6
done
```

### Parallel Execution (Advanced)

```bash
# Run different maxR values in parallel (requires GNU parallel)
parallel python3 exercise9_automate_pipeline.py --maxR {} --skip 4 5 6 ::: 10 20 30 40 50
```

---

## Output Interpretation

### Success Output

```
================================================================================
                        PIPELINE COMPLETED SUCCESSFULLY!                        
================================================================================

Total execution time: 3.16s (0.05 minutes)

Step Results:
  ✓ Exercise 4: Filter Data: SUCCESS
  ✓ Exercise 5: Export Transactions: SUCCESS
  ✓ Exercise 6: Transform to Basket: SUCCESS
  ✓ Exercise 7: Association Rules: SUCCESS

Generated Files:
  ✓ transactions_filtered.txt            1,268,085 bytes
  ✓ transactions_basket.basket             547,597 bytes
  ✓ transactions_basket.tab             17,388,823 bytes
  ✓ exercise7_results_maxR30.txt            11,054 bytes
```

### Partial Success (Skipped Steps)

```
Step Results:
  ⊘ Exercise 4: Filter Data: SKIPPED
  ⊘ Exercise 5: Export Transactions: SKIPPED
  ✓ Exercise 6: Transform to Basket: SUCCESS
  ✓ Exercise 7: Association Rules: SUCCESS
```

### Failure Output

```
✗ SQL script failed with exit code 1
Error output:
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed

Pipeline failed at Exercise 4
```

---

## Performance Optimization

### Skip Unnecessary Steps

If you've already run exercises 4-5 and just want to re-analyze with different parameters:

```bash
# Only re-run Exercise 7 with different maxR
python3 exercise9_automate_pipeline.py --maxR 100 --skip 4 5 6
```

### Reduce Analysis Time

For faster iteration during development:

```bash
# Use lower maxR for quick tests
python3 exercise9_automate_pipeline.py --maxR 10
```

---

## Testing

### Quick Test (Skipping SQL Steps)

```bash
# Test exercises 6 and 7 only
python3 exercise9_automate_pipeline.py --skip 4 5
```

### Dry Run (Prerequisites Only)

Modify script to exit after prerequisites check for validation:

```python
# In exercise9_automate_pipeline.py, after check_prerequisites():
if not check_prerequisites():
    sys.exit(1)
else:
    print("Prerequisites check passed!")
    sys.exit(0)  # Add this line for dry run
```

---

## Troubleshooting

### Enable Verbose Output

The script already provides detailed output. To save logs:

```bash
python3 exercise9_automate_pipeline.py --maxR 30 2>&1 | tee pipeline.log
```

### Check Individual Steps

If pipeline fails, run steps manually:

```bash
# Exercise 4
psql -d db_project_b -f 04_filter_data_exercise4.sql

# Exercise 5
psql -d db_project_b -f 05_export_transactions_exercise5.sql

# Exercise 6
python3 exercise6_transform_to_basket.py

# Exercise 7
python3 exercise7_association_rules.py 30
```

---

## Benefits of Automation

✅ **Consistency:** Same process every time, no manual errors  
✅ **Speed:** 10x faster than running exercises individually  
✅ **Reproducibility:** Complete audit trail of execution  
✅ **Flexibility:** Skip steps, customize parameters  
✅ **Robustness:** Automatic validation and error handling  
✅ **Scalability:** Easy to extend with more exercises  

---

## Future Enhancements

Possible improvements for Exercise 9:

1. **Email notifications** on completion/failure
2. **Slack/Discord integration** for status updates
3. **Docker containerization** for portable execution
4. **Web dashboard** for monitoring pipeline status
5. **Parameterized date ranges** for historical analysis
6. **Multi-dataset support** (analyze multiple months)
7. **Incremental processing** (only process new data)

---

## Files Created

Exercise 9 implementation:

- `scripts/exercise9_automate_pipeline.py` - Main automation script (17 KB)
- `scripts/run_pipeline.sh` - Shell wrapper for convenience
- `EXERCISE_9_GUIDE.md` - This documentation

---

## Summary

Exercise 9 provides a **production-ready automation solution** for the market-basket analysis pipeline. It combines SQL data processing, Python transformation, and Orange association rules analysis into a single, reliable command.

**Key Features:**
- ✅ Full pipeline automation (Exercises 4-7)
- ✅ Flexible execution (skip steps, custom parameters)
- ✅ Comprehensive error handling
- ✅ Detailed progress reporting
- ✅ Output validation
- ✅ Cross-platform support

**Usage:**
```bash
# Full pipeline
python3 exercise9_automate_pipeline.py --maxR 30

# Quick re-analysis
python3 exercise9_automate_pipeline.py --maxR 50 --skip 4 5 6
```

---

**Exercise 9 Complete!** 🎉

The entire PROJECT_B workflow (Exercises 3-9) is now fully implemented and automated!
