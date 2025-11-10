## Classifier prompt — how to run

This project includes `classifier_models.py` which trains three classifiers (One-Rule, Decision Tree and Naive Bayes) and exposes an interactive prompt to make predictions from user input.

### Requirements
- Python 3.8+
- Orange3 (the script uses the Orange library)
- (Optional) the included virtualenv at `PROJECT_A/orange-env`

### Quick steps

1) (Optional) Activate the provided virtual environment:

```bash
source PROJECT_A/orange-env/bin/activate
```

2) Install Orange if not present:

```bash
pip install -U orange3
```

3) Run the interactive prompt:

```bash
python3 PROJECT_A/classifier_models.py
```

#### What the prompt does
- The script loads the dataset `dataset.tab` by default. To use another file, add to the first command argument the dataset file name like this:

```bash
python3 PROJECT_A/classifier_models.py dataset1.tab
```

- It trains One-Rule (a simple categorical rule), a Decision Tree (Orange's TreeLearner) and a Naive Bayes classifier.
- After training it opens an interactive prompt where we enter four comma-separated values matching the dataset attributes in this order:
  age, prescription, astigmatic, tear_rate

#### Valid example input (one line):

```
young,myope,yes,normal
```

#### How to exit
- Type `quit`, `exit` or press Ctrl+C

#### Notes
- With very small datasets the Decision Tree may overfit; we need to use the printed error rates to compare models.
- If we prefer a command-line quick-run (non-interactive) we can edit `classifier_models.py` to expose a small CLI wrapper that calls `one_rule_model()`, `induction_tree_model()` or `naive_bayes_model()` directly.

## Evaluation metrics

The script prints graphs of the hit rates for each model after training. It can execute with the following commands:

Single run default dataset:

```bash
python3 PROJECT_A/compare_models.py 
```

Multiple runs with different datasets (e.g: 10 runs):

```bash
python3 PROJECT_A/compare_models.py --multiple 10
```

Multiple runs with a specific dataset:

```bash
python3 PROJECT_A/compare_models.py --multiple 10 dataset1.tab
```

The script will output the accuracy of each model and plot the results using matplotlib.
