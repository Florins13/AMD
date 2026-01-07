# PROJECT_B - E-Commerce Data Mining Analysis

## Overview
This project involves data mining analysis for We-Commerce's e-commerce platform, focusing on discovering patterns and generating business insights from web analytics data.

## Project Structure

```
PROJECT_B/
├── README.md                           # This file
├── z_dataset_JAN_updated.csv          # Full dataset (~420,000 events)
├── z_datasetSample_JAN.csv            # Sample dataset (first 30 events)
├── z01_aggregatedView.txt             # SQL aggregated views/statistics
├── report_latex/                      # LaTeX report folder
│   ├── report_project_b.tex           # Main LaTeX report
│   └── report_project_b.pdf           # Compiled PDF report
├── _AMD_finalProject_B.pdf            # Project guidelines
└── p_associationRule_extractingKnowledgeUsingMarketBasketAnalysis.pdf

```

## Dataset Information

### Dataset Files
- **z_dataset_JAN_updated.csv**: Complete dataset with 415,863 events collected in January 2012
- **z_datasetSample_JAN.csv**: Sample with 30 events for initial exploration

### Dataset Statistics (from z01_aggregatedView.txt)
- Total events: 415,863
- Total unique visitors (cookie_id): 263,137
- Majority of visitors (240,911) had only 1 session
- Data collected: January 2012

### Dataset Attributes
- `tracking_record_id`: Unique event identifier
- `date_time`: Event timestamp
- `cookie_id`: Visitor's cookie GUID
- `session_id`: Session identifier
- `user_gui`: Registered user identifier
- `product_gui`: Product identifier
- `company`: Product provider company
- `link`: Visited page URL
- `referer`: Referring page URL
- `browser`: Browser identification
- `campaign_id`: Campaign identifier
- `ip`: IP address
- `tracking_id`: Additional tracking info
- `meio`: Medium/channel

## Report Status

### Completed Sections
✅ Introduction and context
✅ Scenario description (We-Commerce business case)
✅ Data collection process explanation
✅ Data quality issues identification
✅ Dataset schema documentation
✅ Business intelligence framework
✅ Methodology descriptions for classification, association rules, and clustering
✅ Technical architecture overview
✅ References section

### TODO Sections (Requiring Code Implementation)

The following sections are marked as TODO in the report and require implementation:

#### 1. Data Statistics (Section 3.2)
- [ ] Exploratory data analysis
- [ ] Temporal distribution analysis
- [ ] Missing value analysis
- [ ] Product view frequency analysis

#### 2. Data Quality Assessment (Section 3.3)
- [ ] Filter useless product_gui values ("open", "home", "/customer/account/login/", etc.)
- [ ] Data cleaning implementation
- [ ] Data validation scripts

#### 3. Feature Engineering (Section 4.2)
- [ ] Extract temporal features (hour, day of week)
- [ ] Calculate session-level metrics
- [ ] Identify returning vs. new visitors
- [ ] Create product category features

#### 4. Data Aggregation (Section 4.3)
- [ ] Session-level aggregation
- [ ] User-level aggregation
- [ ] Product-level aggregation
- [ ] Time-series aggregation

#### 5. Classification Analysis (Section 5.1.2)
- [ ] Implement Decision Trees (J4.8/C4.5, ID3)
- [ ] Implement K-Nearest Neighbors
- [ ] Implement Naive Bayes
- [ ] Model comparison and validation

#### 6. Association Rules Mining (Section 5.2.2)
- [ ] Implement Apriori algorithm
- [ ] Generate frequent itemsets
- [ ] Extract association rules
- [ ] Calculate lift and conviction metrics

#### 7. Clustering Analysis (Section 5.3.2)
- [ ] Implement K-means clustering
- [ ] Perform hierarchical clustering
- [ ] Cluster validation
- [ ] Business interpretation of clusters

#### 8. Model Validation (Section 7.2)
- [ ] Implement train-test split
- [ ] Calculate performance metrics
- [ ] Generate confusion matrices
- [ ] Create ROC curves

#### 9. Experimental Results (Section 7.3)
- [ ] Document classification results
- [ ] Present top association rules
- [ ] Visualize cluster characteristics
- [ ] Create result visualizations

#### 10. Key Findings (Section 8.2)
- [ ] Summarize main discoveries
- [ ] Document business recommendations

#### 11. AI Tool Usage (Section 9.1)
- [ ] Document any use of Generative AI tools
- [ ] Provide links to supporting chats
- [ ] Explain how AI tools were used

#### 12. Appendices
- [ ] Include dataset samples
- [ ] Add code listings
- [ ] Create additional visualizations

## Tools and Technologies

### Required Tools
- **PostgreSQL**: Database management
- **Orange Data Mining**: Interactive data exploration
- **Python**: Algorithm implementation
  - pandas
  - scikit-learn
  - numpy
  - matplotlib
  - seaborn

### LaTeX Compilation
To compile the report to PDF:
```bash
cd report_latex
pdflatex report_project_b.tex
pdflatex report_project_b.tex  # Run twice for TOC
```

## Next Steps

1. **Update Title Page**: Edit the LaTeX file to include your group number and student names/numbers
   
2. **Data Exploration**: Start with exploratory data analysis using the sample dataset
   
3. **Data Cleaning**: Implement scripts to clean and preprocess the data
   
4. **Feature Engineering**: Create derived features for analysis
   
5. **Implement Algorithms**: 
   - Classification models
   - Association rules mining
   - Clustering analysis
   
6. **Document Results**: Fill in TODO sections with findings and visualizations
   
7. **AI Disclosure**: Document any use of AI tools with proper citations
   
8. **Final Review**: Ensure report stays within 10-page limit

## Data Quality Issues to Address

1. **Useless product_gui values**:
   - "open"
   - "home"
   - "/customer/account/login/"
   - "/customer/account/forgotpassword/"
   - Other navigation/system pages

2. **Dynamic IP addresses**: Less reliable for visitor tracking

3. **Missing values**: Some fields may be empty for certain events

## Submission Requirements

Per project guidelines:
- Maximum 10 pages for main report
- First page must include: discipline name, course name, title, group number, student names and numbers
- File naming: `AMD_DorN_XX.zip` where XX is the group number
- Include: report PDF, all code files (.py), data files (.tab), execution scripts (.sh/.bat), README.txt with execution instructions
- **IMPORTANT**: Cite all Generative AI tool usage with supporting chat links

## Contact & Collaboration

- Update the title page with your group information
- Coordinate task assignments among team members
- Track progress on TODO items
- Document all code and findings clearly

---

**Last Updated**: January 4, 2026
**Report Location**: [report_latex/report_project_b.pdf](report_latex/report_project_b.pdf)
