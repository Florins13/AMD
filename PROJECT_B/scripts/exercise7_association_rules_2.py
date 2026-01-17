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


# ===============================
# HELPER FUNCTIONS
# ===============================

def generate_rules_with_config(X, min_support_count, confidence):
    """
    Run the FP-Growth algorithm with ABSOLUTE support count.
    """
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


def find_optimal_config(X, support_range, confidence_range, config_name):
    """
    THE GRID SEARCH ENGINE
    """
    print(f"\n[{config_name}] Starting Grid Search...")
    print(f"   Testing {len(support_range)} supports x {len(confidence_range)} confidences...")
    
    best_config = None
    best_score = float('inf') 
    
    for support_count in support_range:
        for confidence in confidence_range:
            _, rules = generate_rules_with_config(X, support_count, confidence)
            num_rules = len(rules)
            
            # Scoring Logic
            if num_rules <= TARGET_RULES_MAX:
                score = TARGET_RULES_MAX - num_rules 
            else:
                score = 1000 + (num_rules - TARGET_RULES_MAX)
            
            if best_config is None or score < best_score:
                best_score = score
                best_config = (support_count, confidence, num_rules)
    
    if best_config:
        s, c, n = best_config
        # s is now an integer (count)
        print(f"   ✓ WINNER: Supp={s} (Count), Conf={c*100:.0f}% -> {n} Rules")
        return best_config
    
    return None


def plot_association_rules(list_setOf_rule, Xbasket, mapping, title, figure_num):
    """
    Visualizes the rules as a Scatter Plot.
    X-Axis = Absolute Support (Count)
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
    # X-Axis: Standard Integer (No percentage)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True)) # Force integers
    
    # Y-Axis: Percentage
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))

    ax.set_xlabel('Support (Transaction Count)', fontsize=12)
    ax.set_ylabel('Confidence (%)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)

    figures_dir = "../figures"
    os.makedirs(figures_dir, exist_ok=True)
    filename = f"{figures_dir}/figure_{figure_num}_rules.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"   [Plot] Saved Figure {figure_num} to {filename}")


def save_results_to_file(Xbasket, mapping, support_count, confidence,
                         dict_setOf_itemset, list_setOf_rule, output_filename):
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


def generate_all_figures(Xbasket, X, mapping):
    
    # --- CONFIG 1 ---
    print("\n" + "="*50)
    print("CONFIG 1: Products to Keep Together")
    best_1 = find_optimal_config(X, SUPPORT_RANGE_CONFIG_1, CONFIDENCE_RANGE_CONFIG_1, "Config 1")
    
    if best_1:
        sup_cnt, conf, _ = best_1
        itemsets, rules = generate_rules_with_config(X, sup_cnt, conf)
        plot_association_rules(rules, Xbasket, mapping, 
                             f"Q1: Keep Together (Supp={sup_cnt}, Conf={conf*100:.0f}%)", 1)
        save_results_to_file(Xbasket, mapping, sup_cnt, conf, 
                           itemsets, rules, "results_config_1.txt")


    # --- CONFIG 2 ---
    print("\n" + "="*50)
    print("CONFIG 2: Rare but Strong")
    best_2 = find_optimal_config(X, SUPPORT_RANGE_CONFIG_2, CONFIDENCE_RANGE_CONFIG_2, "Config 2")
    
    if best_2:
        sup_cnt, conf, _ = best_2
        itemsets, rules = generate_rules_with_config(X, sup_cnt, conf)
        plot_association_rules(rules, Xbasket, mapping, 
                             f"Q2: Rare Strong (Supp={sup_cnt}, Conf={conf*100:.0f}%)", 2)
        save_results_to_file(Xbasket, mapping, sup_cnt, conf, 
                           itemsets, rules, "results_config_2.txt")


    # --- CONFIG 3 ---
    print("\n" + "="*50)
    print("CONFIG 3: Most Visited")
    best_3 = find_optimal_config(X, SUPPORT_RANGE_CONFIG_3, CONFIDENCE_RANGE_CONFIG_3, "Config 3")
    
    if best_3:
        sup_cnt, conf, _ = best_3
        itemsets, rules = generate_rules_with_config(X, sup_cnt, conf)
        plot_association_rules(rules, Xbasket, mapping, 
                             f"Q3: Most Visited (Supp={sup_cnt}, Conf={conf*100:.0f}%)", 3)
        save_results_to_file(Xbasket, mapping, sup_cnt, conf, 
                           itemsets, rules, "results_config_3.txt")


def main():
    global TARGET_RULES_MAX

    parser = argparse.ArgumentParser(description='Market Basket Analysis with Grid Search')
    parser.add_argument('max_rules', nargs='?', type=int, default=10, 
                        help='Target maximum number of rules to find (Default: 10)')
    
    args = parser.parse_args()
    TARGET_RULES_MAX = args.max_rules

    print("Starting Exercise 7 - Grid Search Analysis (Absolute Support Counts)...")
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
    
    generate_all_figures(Xbasket, X, mapping)
    
    print("\nAnalysis Complete. Check 'figures/' and 'results/' folders.")

if __name__ == "__main__":
    main()