# EXERCISE 8 - ORANGE GRAPHICAL REPORT GUIDE
## Market-Basket Analysis Report for We-Commerce

**Objective:** Create a visual, graphical report using Orange Data Mining to present association rules analysis results to We-Commerce stakeholders.

---

## OPTION 1: QUICK START - Copy Reference Workflow

### Step 1: Copy the PRACTICE_7 workflow as starting point

```bash
cd /home/guerra38/ISEL/AMD/2526/AMD/PROJECT_B
cp ../PRACTICE_7/z_workflow_associationRules.ows orange_workflow_exercise8.ows
```

### Step 2: Launch Orange and open the workflow

```bash
# Make sure Orange is installed
orange-canvas orange_workflow_exercise8.ows
```

### Step 3: Adapt the workflow for PROJECT_B data

1. **Replace File widgets** to point to:
   - `transactions_basket.basket` (your We-Commerce data)
   - `transactions_basket.tab` (alternative format)

2. **Configure widgets** with Exercise 7 optimal parameters:
   - Support: 0.30% (14 transactions)
   - Confidence: 65%

3. **Add visualization widgets:**
   - Scatter Plot (Confidence vs Support)
   - Data Table (to show rules)
   - Box Plot (for itemset sizes)

---

## OPTION 2: BUILD FROM SCRATCH - Step-by-Step Guide

### Step 1: Launch Orange

```bash
cd /home/guerra38/ISEL/AMD/2526/AMD/PROJECT_B
orange-canvas
```

### Step 2: Create the Workflow

#### A. Load Data
1. Add **File** widget from Data category
2. Click on File widget, browse to: `transactions_basket.basket`
3. Verify it shows: 4945 instances, 1750 features

#### B. View Data Table
1. Add **Data Table** widget
2. Connect: File → Data Table
3. This lets you inspect the basket data

#### C. Find Frequent Itemsets
1. Add **Frequent Itemsets** widget (from Associate add-on)
2. Connect: Data Table → Frequent Itemsets
3. Configure:
   - Minimal support: 14 (0.30% of 4945)
   - Or use percentage: 0.3%
4. Output shows 72 frequent itemsets (as found in Exercise 7)

#### D. Generate Association Rules
1. Add **Association Rules** widget (from Associate add-on)
2. Connect: Frequent Itemsets → Association Rules
3. Configure:
   - Minimal confidence: 0.65 (65%)
   - Max rules: 30
4. Output should show ~26 rules

#### E. Add Visualizations
1. **Scatter Plot**:
   - Connect: Association Rules → Scatter Plot
   - X-axis: Support
   - Y-axis: Confidence
   - Color: Lift (or rule strength)
   - Shows which rules are strongest

2. **Data Table (for rules)**:
   - Connect: Association Rules → Data Table
   - Shows all 26 rules in tabular format
   - Can export to CSV/Excel

3. **Save Image**:
   - Connect: Association Rules → Save Image
   - Exports visualization as PNG/PDF for report

---

## OPTION 3: PROGRAMMATIC APPROACH (Python + Orange)

If you prefer to automate report generation:

### Create a report generation script

```python
# See: scripts/exercise8_generate_orange_report.py (will create next)
```

---

## RECOMMENDED WORKFLOW STRUCTURE

```
[File] ──→ [Data Table] ──→ [Frequent Itemsets] ──→ [Association Rules]
                                    │                        │
                                    ↓                        ↓
                            [Data Table (itemsets)]  [Data Table (rules)]
                                                             │
                                                             ↓
                                                      [Scatter Plot]
                                                             │
                                                             ↓
                                                       [Save Image]
```

---

## KEY CONFIGURATION VALUES (from Exercise 7)

Use these exact values to reproduce Exercise 7 findings:

- **Dataset:** `transactions_basket.basket` (4,945 transactions)
- **Minimum Support:** 14 transactions (0.30%)
- **Minimum Confidence:** 0.65 (65%)
- **Expected Itemsets:** 72
- **Expected Rules:** 26

---

## REPORT ELEMENTS TO INCLUDE

### 1. Overview Statistics
- Total transactions: 4,945
- Unique products: 1,750
- Analysis period: January 2012
- Filter applied: 5-30 sessions per visitor

### 2. Frequent Itemsets Table
- Show top 20 itemsets by support
- Include: itemset, support count, support %

### 3. Association Rules Table
- Show all 26 rules
- Columns: Antecedent, Consequent, Support, Confidence, Lift
- Sort by confidence (descending)

### 4. Visualizations
- **Scatter Plot:** Confidence vs Support (with rule density)
- **Bar Chart:** Top 10 most visited products
- **Network Graph:** Product associations (if Orange supports it)
- **Lift Chart:** Rules with highest lift values

### 5. Business Insights Section
- Key finding: iPad ↔ iPod Touch (100% confidence)
- Homepage dominance: 294 visits (6%)
- Luis Onofre brand strength

---

## SCREENSHOTS TO CAPTURE

For the We-Commerce report, capture these views:

1. **Workflow Overview** (entire canvas with all widgets)
2. **Data Table** (showing basket format)
3. **Frequent Itemsets Widget** (configured with support=0.3%)
4. **Association Rules Widget** (showing 26 rules)
5. **Scatter Plot** (Confidence vs Support)
6. **Top Rules Table** (sorted by confidence)
7. **Product Network** (if available)

---

## EXPORTING THE REPORT

### From Orange GUI:
1. **File → Report** (generates HTML report)
2. **Right-click widget → Save Image** (for individual visualizations)
3. **Data Table → Export to Excel** (for rules table)

### For We-Commerce Presentation:
1. Save workflow as: `orange_workflow_exercise8.ows`
2. Export visualizations to: `exercise8_visualizations/`
3. Create PowerPoint/PDF with:
   - Title slide
   - Methodology (workflow diagram)
   - Results (tables and charts)
   - Recommendations (from Exercise 7)

---

## TROUBLESHOOTING

### Issue: Orange doesn't open .basket files
**Solution:** Basket files should work directly. If not, use the .tab format:
```python
# In File widget, select: transactions_basket.tab
```

### Issue: No Association Rules widget
**Solution:** Install Orange Associate add-on:
```bash
pip install Orange3-Associate
# Or in Orange: Options → Add-ons → Install Orange3-Associate
```

### Issue: Too many rules (overwhelming)
**Solution:** Increase confidence threshold:
- Try 70%, 75%, 80% to reduce rules
- Or increase support to 0.5%, 1%

### Issue: Too few rules
**Solution:** Decrease support threshold:
- Try 0.2%, 0.1% to find more patterns
- But be careful of noise

---

## NEXT STEPS AFTER CREATING WORKFLOW

1. **Save the workflow:** `orange_workflow_exercise8.ows`
2. **Export visualizations** as PNG/PDF
3. **Document findings** in PowerPoint/Word
4. **Add business interpretations** from Exercise 7
5. **Create executive summary** for We-Commerce

---

## ALTERNATIVE: Automated Report Script

If you want a fully automated Python script instead of GUI:

**Option A:** Use Orange Python API (like Exercise 7)
**Option B:** Create HTML report with matplotlib/plotly
**Option C:** Generate LaTeX report with embedded images

Let me know which approach you prefer!

---

## QUICK COMMANDS REFERENCE

```bash
# Copy reference workflow
cp ../PRACTICE_7/z_workflow_associationRules.ows orange_workflow_exercise8.ows

# Launch Orange
orange-canvas orange_workflow_exercise8.ows

# Or start fresh
orange-canvas

# Install Orange (if needed)
pip install Orange3 Orange3-Associate

# Check Orange version
python3 -c "import Orange; print(Orange.__version__)"
```

---

## EXPECTED OUTPUT FILES

After completing Exercise 8:

- `orange_workflow_exercise8.ows` - Orange workflow file
- `exercise8_visualizations/` - Folder with exported images
  - `scatter_confidence_support.png`
  - `top_products_barchart.png`
  - `association_rules_table.png`
  - `workflow_overview.png`
- `exercise8_report.pdf` - Final report for We-Commerce
- `exercise8_report.pptx` - Presentation slides (optional)

---

## ESTIMATED TIME

- **GUI Approach:** 30-45 minutes (interactive, learning curve)
- **Copy & Adapt:** 15-20 minutes (using PRACTICE_7 workflow)
- **Python Script:** 45-60 minutes (fully automated)

**Recommendation:** Start with GUI to understand the process, then automate if needed.
