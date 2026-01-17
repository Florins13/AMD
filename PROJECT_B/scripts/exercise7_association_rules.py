# -*- coding: utf-8 -*-
# ===============================
# Exercise 7 - Association Rules (Data-Calibrated Absolute Support)
# Market-Basket Analysis for We-Commerce
# ===============================

import Orange
from orangecontrib.associate.fpgrowth import *
import os
import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import PercentFormatter

# Use non-interactive backend for saving figures without display window
matplotlib.use('Agg')

# ===============================
# CONFIGURATION & GRID SEARCH PARAMETERS
# ===============================

BASKET_FILE = "../transactions_basket.basket"
TARGET_RULES_MAX = 10
TOTAL_TRANSACTIONS = 3048  # Used for percentage calculations

# --- GRID SEARCH ARRAYS (ABSOLUTE COUNTS BASED ON YOUR DATA) ---
# Total Transactions: 3048
# Top Item Frequency: 127

# Configuration 1: "Products to keep together" (Mid-Tier Interactions)
# Strategy: Look for solid, repeatable patterns (15-35 transactions)
# Confidence: 40-60% (Good correlation)
SUPPORT_RANGE_CONFIG_1 = [10, 15, 20, 25, 30]
CONFIDENCE_RANGE_CONFIG_1 = [0.40, 0.45, 0.50, 0.55, 0.60]

# Configuration 2: "Rare but Strong" (Niche/Long Tail)
# Strategy: Look for rare items (6-12 transactions) that are almost ALWAYS bought together.
# Confidence: 70-90% (Very strong correlation)
SUPPORT_RANGE_CONFIG_2 = [6, 7, 8, 10, 12]
CONFIDENCE_RANGE_CONFIG_2 = [0.70, 0.75, 0.80, 0.85, 0.90]

# Configuration 3: "Most Visited Products" (Top Sellers)
# Strategy: Look for your top movers (40+ transactions).
# Confidence: 10-30% (Popular items often have lower direct confidence because they are bought with everything)
SUPPORT_RANGE_CONFIG_3 = [20, 25, 30, 35, 40]  # Note: Adjusted for absolute counts
CONFIDENCE_RANGE_CONFIG_3 = [0.0005, 0.001, 0.005, 0.01, 0.05]  # Note: Very low confidence due to popularity

# --- PERCENTAGE-BASED SUPPORT RANGES (3048 transactions) ---
# Config 1: 0.3% to 1.0% (approximately 9 to 30 transactions)
SUPPORT_PERCENT_RANGE_CONFIG_1 = [0.003, 0.004, 0.005, 0.007, 0.010]
CONFIDENCE_PERCENT_RANGE_CONFIG_1 = [0.40, 0.45, 0.50, 0.55, 0.60]

# Config 2: 0.2% to 0.4% (approximately 6 to 12 transactions)
SUPPORT_PERCENT_RANGE_CONFIG_2 = [0.002, 0.0025, 0.003, 0.0035, 0.004]
CONFIDENCE_PERCENT_RANGE_CONFIG_2 = [0.70, 0.75, 0.80, 0.85, 0.90]

# Config 3: 0.7% to 1.3% (approximately 20 to 40 transactions)
SUPPORT_PERCENT_RANGE_CONFIG_3 = [0.007, 0.008, 0.010, 0.012, 0.013]
CONFIDENCE_PERCENT_RANGE_CONFIG_3 = [0.0005, 0.001, 0.005, 0.01, 0.05]


# ===============================
# HELPER FUNCTIONS
# ===============================

def generate_rules_with_config(X, min_support_count, confidence, use_percentage=False, total_trans=None):
    """
    Run the FP-Growth algorithm with ABSOLUTE support count or PERCENTAGE.
    """
    if use_percentage:
        # Convert percentage to absolute count
        if total_trans is None:
            raise ValueError("total_trans required when use_percentage=True")
        min_support = max(2, int(min_support_count * total_trans))
    else:
        # Ensure min_support is at least 2 transactions
        min_support = max(2, int(min_support_count))
    
    # Pass integer directly to frequent_itemsets for absolute count support
    setOf_itemset = frequent_itemsets(X, min_support)
    dict_setOf_itemset = dict(setOf_itemset)
    
    if len(dict_setOf_itemset) == 0:
        return dict_setOf_itemset, []
    
    setOf_rule = association_rules(dict_setOf_itemset, confidence)
    list_setOf_rule = list(setOf_rule)
    
    return dict_setOf_itemset, list_setOf_rule


def find_optimal_config(X, support_range, confidence_range, config_name, use_percentage=False, total_trans=None):
    """
    THE GRID SEARCH ENGINE
    """
    print(f"\n[{config_name}] Starting Grid Search...")
    print(f"   Testing {len(support_range)} supports x {len(confidence_range)} confidences...")
    
    best_config = None
    best_score = float('inf') 
    
    for support_val in support_range:
        for confidence in confidence_range:
            _, rules = generate_rules_with_config(X, support_val, confidence, use_percentage, total_trans)
            num_rules = len(rules)
            
            # Scoring Logic
            if num_rules <= TARGET_RULES_MAX:
                score = TARGET_RULES_MAX - num_rules 
            else:
                score = 1000 + (num_rules - TARGET_RULES_MAX)
            
            if best_config is None or score < best_score:
                best_score = score
                best_config = (support_val, confidence, num_rules)
    
    if best_config:
        s, c, n = best_config
        if use_percentage:
            actual_count = int(s * total_trans) if total_trans else 0
            print(f"   ✓ WINNER: Supp={s*100:.2f}% (~{actual_count} trans), Conf={c*100:.0f}% -> {n} Rules")
        else:
            print(f"   ✓ WINNER: Supp={s} (Count), Conf={c*100:.0f}% -> {n} Rules")
        return best_config
    
    return None


def plot_association_rules(list_setOf_rule, Xbasket, mapping, title, figure_num, use_percentage=False, total_trans=None):
    """
    Visualizes the rules as a Scatter Plot.
    X-Axis = Absolute Support (Count) or Percentage
    Y-Axis = Confidence (%)
    """
    if not list_setOf_rule:
        print(f"WARNING: No rules to plot for Figure {figure_num}")
        return

    supports = []
    confidences = []
    rule_labels = []

    for i, (LHS, RHS, supp, conf) in enumerate(list_setOf_rule, 1):
        # supp is already the absolute count coming from Orange
        if use_percentage and total_trans:
            supports.append((supp / total_trans) * 100)  # Convert to percentage for display
        else:
            supports.append(supp)
        confidences.append(conf * 100) # Scale confidence to 0-100 for formatting
        
        decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        
        def clean_name(n): return n.split('=')[-1] if '=' in n else n
        lhs_str = ", ".join([clean_name(n) for n in decoded_LHS])
        rhs_str = ", ".join([clean_name(n) for n in decoded_RHS])
        
        label = f"R{i}: {lhs_str[:15]} -> {rhs_str[:15]}"
        rule_labels.append(label)

    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = ['red' if c == 100.0 else 'orange' if c >= 90.0 else 'blue' for c in confidences]
    
    ax.scatter(supports, confidences, alpha=0.6, s=100, c=colors, edgecolors='black')

    for supp, conf, label in zip(supports, confidences, rule_labels):
        ax.annotate(label, (supp, conf), xytext=(5, 5), textcoords='offset points', fontsize=8)

    # AXIS FORMATTING
    if use_percentage:
        # X-Axis: Percentage
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=2))
        ax.set_xlabel('Support (%)', fontsize=12)
    else:
        # X-Axis: Standard Integer (No percentage)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True)) # Force integers
        ax.set_xlabel('Support (Transaction Count)', fontsize=12)
    
    # Y-Axis: Percentage
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))

    ax.set_ylabel('Confidence (%)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)

    plots_dir = "../plots"
    os.makedirs(plots_dir, exist_ok=True)
    suffix = "_percent" if use_percentage else "_count"
    filename = f"{plots_dir}/figure_{figure_num}_rules{suffix}.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"   [Plot] Saved Figure {figure_num} to {filename}")


def save_results_to_file(Xbasket, mapping, support_count, confidence,
                         dict_setOf_itemset, list_setOf_rule, output_filename, use_percentage=False):
    """
    Writes the detailed rule text to a file.
    """
    results_dir = "../results"
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, output_filename)

    total_trans = len(Xbasket)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"RESULTS FOR CONFIGURATION: {output_filename}\n")
        f.write("=" * 60 + "\n\n")
        if use_percentage:
            actual_count = int(support_count * total_trans)
            f.write(f"Parameters: Min Support={support_count*100:.2f}% (~{actual_count} trans), Confidence={confidence:.0%}\n")
        else:
            f.write(f"Parameters: Min Support={support_count} (Count), Confidence={confidence:.0%}\n")
        f.write(f"Total Transactions: {total_trans}\n")
        f.write(f"Rules Found: {len(list_setOf_rule)}\n")
        f.write("-" * 60 + "\n\n")

        # Sort rules by Confidence desc, then Support desc
        rules_sorted = sorted(list_setOf_rule, key=lambda x: (x[3], x[2]), reverse=True)

        for i, (LHS, RHS, supp, conf) in enumerate(rules_sorted, 1):
            decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
            decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
            
            # Calculate % for the report just for reference
            supp_pct = (supp / total_trans) * 100

            f.write(f"Rule {i}:\n")
            f.write(f"   IF:   {decoded_LHS}\n")
            f.write(f"   THEN: {decoded_RHS}\n")
            f.write(f"   Stats: Conf={conf:.2%}, Supp={supp} ({supp_pct:.2f}%)\n\n")

    print(f"   [Report] Saved text results to {filepath}")


def generate_all_figures(Xbasket, X, mapping, use_percentage=False):
    total_trans = len(Xbasket)
    
    if use_percentage:
        supp_range_1 = SUPPORT_PERCENT_RANGE_CONFIG_1
        conf_range_1 = CONFIDENCE_PERCENT_RANGE_CONFIG_1
        supp_range_2 = SUPPORT_PERCENT_RANGE_CONFIG_2
        conf_range_2 = CONFIDENCE_PERCENT_RANGE_CONFIG_2
        supp_range_3 = SUPPORT_PERCENT_RANGE_CONFIG_3
        conf_range_3 = CONFIDENCE_PERCENT_RANGE_CONFIG_3
        suffix = "_percent"
    else:
        supp_range_1 = SUPPORT_RANGE_CONFIG_1
        conf_range_1 = CONFIDENCE_RANGE_CONFIG_1
        supp_range_2 = SUPPORT_RANGE_CONFIG_2
        conf_range_2 = CONFIDENCE_RANGE_CONFIG_2
        supp_range_3 = SUPPORT_RANGE_CONFIG_3
        conf_range_3 = CONFIDENCE_RANGE_CONFIG_3
        suffix = "_count"
    
    # --- CONFIG 1 ---
    print("\n" + "="*50)
    print("CONFIG 1: Products to Keep Together")
    best_1 = find_optimal_config(X, supp_range_1, conf_range_1, "Config 1", use_percentage, total_trans)
    
    if best_1:
        sup_val, conf, _ = best_1
        itemsets, rules = generate_rules_with_config(X, sup_val, conf, use_percentage, total_trans)
        if use_percentage:
            title = f"Q1: Keep Together (Supp={sup_val*100:.2f}%, Conf={conf*100:.0f}%)"
        else:
            title = f"Q1: Keep Together (Supp={sup_val}, Conf={conf*100:.0f}%)"
        plot_association_rules(rules, Xbasket, mapping, title, 1, use_percentage, total_trans)
        save_results_to_file(Xbasket, mapping, sup_val, conf, 
                           itemsets, rules, f"results_config_1{suffix}.txt", use_percentage)


    # --- CONFIG 2 ---
    print("\n" + "="*50)
    print("CONFIG 2: Rare but Strong")
    best_2 = find_optimal_config(X, supp_range_2, conf_range_2, "Config 2", use_percentage, total_trans)
    
    if best_2:
        sup_val, conf, _ = best_2
        itemsets, rules = generate_rules_with_config(X, sup_val, conf, use_percentage, total_trans)
        if use_percentage:
            title = f"Q2: Rare Strong (Supp={sup_val*100:.2f}%, Conf={conf*100:.0f}%)"
        else:
            title = f"Q2: Rare Strong (Supp={sup_val}, Conf={conf*100:.0f}%)"
        plot_association_rules(rules, Xbasket, mapping, title, 2, use_percentage, total_trans)
        save_results_to_file(Xbasket, mapping, sup_val, conf, 
                           itemsets, rules, f"results_config_2{suffix}.txt", use_percentage)


    # --- CONFIG 3 ---
    print("\n" + "="*50)
    print("CONFIG 3: Most Visited")
    best_3 = find_optimal_config(X, supp_range_3, conf_range_3, "Config 3", use_percentage, total_trans)
    
    if best_3:
        sup_val, conf, _ = best_3
        itemsets, rules = generate_rules_with_config(X, sup_val, conf, use_percentage, total_trans)
        if use_percentage:
            title = f"Q3: Most Visited (Supp={sup_val*100:.2f}%, Conf={conf*100:.0f}%)"
        else:
            title = f"Q3: Most Visited (Supp={sup_val}, Conf={conf*100:.0f}%)"
        plot_association_rules(rules, Xbasket, mapping, title, 3, use_percentage, total_trans)
        save_results_to_file(Xbasket, mapping, sup_val, conf, 
                           itemsets, rules, f"results_config_3{suffix}.txt", use_percentage)


def main():
    global TARGET_RULES_MAX

    parser = argparse.ArgumentParser(description='Market Basket Analysis with Grid Search')
    parser.add_argument('max_rules', nargs='?', type=int, default=10, 
                        help='Target maximum number of rules to find (Default: 10)')
    parser.add_argument('--percentage', '-p', action='store_true',
                        help='Use percentage-based support instead of absolute counts')
    
    args = parser.parse_args()
    TARGET_RULES_MAX = args.max_rules
    use_percentage = args.percentage

    support_mode = "Percentage" if use_percentage else "Absolute Support Counts"
    print(f"Starting Exercise 7 - Grid Search Analysis ({support_mode})...")
    print(f"Targeting max {TARGET_RULES_MAX} rules per configuration.")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if not os.path.exists(BASKET_FILE):
        print(f"ERROR: File not found: {BASKET_FILE}")
        return

    try:
        Xbasket = Orange.data.Table(BASKET_FILE)
        print(f"Dataset Loaded: {len(Xbasket)} transactions.")
    except Exception as e:
        print(f"Error loading Orange Table: {e}")
        return

    print("One-Hot Encoding data...")
    X, mapping = OneHot.encode(Xbasket, include_class=False)
    
    generate_all_figures(Xbasket, X, mapping, use_percentage)
    
    print("\nAnalysis Complete. Check 'plots/' and 'results/' folders.")

if __name__ == "__main__":
    main()