# AMD Final Project A1 - Mushroom Classification

This project analyzes a mushroom dataset to classify mushrooms as edible or poisonous using machine learning techniques, including the 1R algorithm and Orange Data Mining tools.

## 📁 Project Structure

```
PROJECT_A1/
├── dataset_long_name_ORIGINAL.csv          # Original mushroom dataset
├── dataset_description.txt                  # Dataset attribute descriptions
├── dataset_long_name_CONVERTED.tab         # Converted dataset for Orange
├── dataset_long_name_PTS_INPUT_v01.tab     # Alternative Orange format dataset
├── dataset_converter.py                     # Script to convert CSV to .tab format
├── one_rule.py                             # 1R algorithm implementation
├── classifier_handler.py                    # Main script for 1R execution
├── oneR_OUTPUT.txt                         # 1R algorithm output results
├── for_A1.ows                              # Orange Data Mining workflow
└── report_latex/                           # LaTeX report directory
    ├── report.tex                          # Main LaTeX document
    ├── report.pdf                          # Compiled PDF report
    └── figures/                            # Report figures
```

## 🔧 Prerequisites

### Python Requirements
- Python 3.10 or higher
- Orange3 library
- NumPy

Install dependencies:
```bash
pip install Orange3 numpy
```

### Orange Data Mining
Download and install Orange from: https://orangedatamining.com/

## 🔄 Exercise 2: Data Transformation

### Objective
Transform the original CSV dataset into Orange's `.tab` format for proper processing in Orange Data Mining.

### Running the Conversion

```bash
cd PROJECT_A1
python3.10 dataset_converter.py
```

### What the Script Does
The `dataset_converter.py` script:
1. Loads the CSV file using Orange's data reader
2. Automatically converts it to `.tab` format
3. Saves as `dataset_long_name_CONVERTED.tab`

### Output
- `dataset_long_name_CONVERTED.tab` - Dataset ready for Orange processing

## 🎯 Exercise 3: 1R Algorithm Application

### Objective
Apply the 1R (One Rule) classification algorithm to find the single best attribute for predicting mushroom edibility.

### Running the 1R Algorithm

```bash
cd PROJECT_A1
python3.10 classifier_handler.py
```

### What Happens
1. Loads the converted dataset (`dataset_long_name_CONVERTED.tab`)
2. Splits data into training (80%) and testing (20%) sets
3. Applies the 1R algorithm to find the best predictive attribute
4. Generates detailed statistics for each attribute value
5. Saves results to `oneR_OUTPUT.txt`

### Output Format
The output file contains:
```
(attr, valueAttr, valueTarget) : (error, total)
```

## 🍊 Exercise 4: Orange Data Mining Exploration

### Objective
Use Orange Data Mining to visualize the dataset, train classifiers (Tree and Random Forest), and compare predictions.

### Opening the Orange Workflow

1. **Launch Orange Data Mining**

2. **Open the prepared workflow:**
   - Click `File` → `Open`
   - Select `for_A1.ows`

3. **If dataset doesn't load automatically:**
   - Click on the `File` widget in the pipeline
   - Select `dataset_long_name_PTS_INPUT_v01.tab`

4. **Explore the widgets:**
   - **Data Table** - View dataset instances
   - **Distributions** - See class distribution
   - **Tree** - Decision tree classifier
   - **Random Forest** - Ensemble classifier
   - **Confusion Matrix** - Evaluate predictions
   - **Pythagorean Forest** - Visualize random forest trees

### Key Findings from Orange
- **Dataset:** 8416 instances confirmed
- **Distribution:** 53.33% edible, 46.67% poisonous
- **Tree Classifier:** High accuracy, also selected `odor` as root
- **Random Forest:** Perfect classification (100% accuracy on test set)

## 👥 Authors

- Florin Sofinet (A46608)
- Diogo Guerra (A49149)
- Nuno Silva (A53976)

**Course:** Aprendizagem e Mineração de Dados (AMD)  
**Semester:** 1º Semestre – 2025/2026  
**Institution:** Instituto Superior de Engenharia de Lisboa (ISEL)