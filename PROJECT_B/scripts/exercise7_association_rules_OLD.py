# -*- coding: utf-8 -*-
# ===============================
# Exercise 7 - Association Rules
# Market-Basket Analysis for We-Commerce
# ===============================

import Orange
from orangecontrib.associate.fpgrowth import *
import os
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving figures

# Dataset path
BASKET_FILE = "../transactions_basket.basket"

# ===============================
# GRID SEARCH PARAMETERS
# ===============================

# Support range (as percentages)
SUPPORT_RANGE_CONFIG_1 = [0.0025, 0.0030, 0.0033, 0.0040, 0.0050]  # Low-moderate support
SUPPORT_RANGE_CONFIG_2 = [0.0016, 0.0020, 0.0025, 0.0030]          # Low support
SUPPORT_RANGE_CONFIG_3 = [0.0050, 0.0065, 0.0080, 0.0100, 0.0130]  # High support

# Confidence range (as decimals)
CONFIDENCE_RANGE_CONFIG_1 = [0.40, 0.45, 0.50, 0.55, 0.60]         # Moderate confidence
CONFIDENCE_RANGE_CONFIG_2 = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]   # High confidence
CONFIDENCE_RANGE_CONFIG_3 = [0.10, 0.15, 0.20, 0.25, 0.30]         # Very low confidence (almost 0)

# Maximum number of rules for optimization
TARGET_RULES_MAX = 10


def generate_rules_with_config(X, support_pct, confidence):
    """
    Generate association rules with a specific support and confidence configuration.
    
    Args:
        X: OneHot encoded dataset
        support_pct: Support threshold (as decimal, e.g., 0.004 for 0.4%)
        confidence: Confidence threshold (as decimal, e.g., 0.65 for 65%)
    
    Returns:
        Tuple of (dict_setOf_itemset, list_setOf_rule)
    """
    total_transactions = len(X)
    min_support = max(2, int(total_transactions * support_pct))
    
    print(f"Support={support_pct:.2%} ({min_support} trans), Confidence={confidence:.2%}", end="")
    
    # Find frequent itemsets
    setOf_itemset = frequent_itemsets(X, min_support)
    dict_setOf_itemset = dict(setOf_itemset)
    
    if len(dict_setOf_itemset) == 0:
        print(" -> 0 rules")
        return dict_setOf_itemset, []
    
    # Generate association rules
    setOf_rule = association_rules(dict_setOf_itemset, confidence)
    list_setOf_rule = list(setOf_rule)
    
    print(f" -> {len(list_setOf_rule)} rules")
    
    return dict_setOf_itemset, list_setOf_rule

def plot_association_rules(list_setOf_rule, Xbasket, mapping, title, figure_num):
    """
    Create scatter plot of association rules (support vs confidence).
    Also print decoded rules to terminal.
    """
    if not list_setOf_rule:
        print(f"No rules to plot for Figure {figure_num}")
        return
    
    # Extract support and confidence values and decode rules
    supports = []
    confidences = []
    rule_labels = []
    
    for i, (LHS, RHS, supp, conf) in enumerate(list_setOf_rule, 1):
        # Convert absolute support to relative support (proportion)
        relative_support = supp / len(Xbasket)
        supports.append(relative_support)
        confidences.append(conf)
        
        # Decode LHS and RHS
        decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        
        # Create short label for the rule
        # Shorten product names for readability
        lhs_short = [p.split('*')[-1][:15] for p in decoded_LHS]
        rhs_short = [p.split('*')[-1][:15] for p in decoded_RHS]
        
        if len(lhs_short) == 1 and len(rhs_short) == 1:
            label = f"R{i}: {lhs_short[0]}→{rhs_short[0]}"
        else:
            lhs_str = ','.join(lhs_short[:2])
            if len(lhs_short) > 2:
                lhs_str += f"+{len(lhs_short)-2}"
            rhs_str = ','.join(rhs_short[:2])
            if len(rhs_short) > 2:
                rhs_str += f"+{len(rhs_short)-2}"
            label = f"R{i}: [{lhs_str}]→[{rhs_str}]"
        
        rule_labels.append(label)
    
    # Create figure with larger size to accommodate annotations
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create scatter plot with different colors based on confidence
    colors = ['red' if c == 1.0 else 'orange' if c >= 0.95 else 'blue' for c in confidences]
    scatter = ax.scatter(supports, confidences, alpha=0.7, s=150, c=colors, edgecolors='black', linewidths=1.5)
    
    # Add annotations for each point
    for i, (supp, conf, label) in enumerate(zip(supports, confidences, rule_labels)):
        # Adjust text position to avoid overlap
        offset_x = 2
        offset_y = 0.01
        
        ax.annotate(label, 
                   xy=(supp, conf), 
                   xytext=(offset_x, offset_y),
                   textcoords='offset points',
                   fontsize=8,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7, edgecolor='black'),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=0.5))
    
    ax.set_xlabel('Support (relative proportion)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Confidence', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='Confidence = 100%'),
        Patch(facecolor='orange', edgecolor='black', label='Confidence ≥ 95%'),
        Patch(facecolor='blue', edgecolor='black', label='Confidence < 95%')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    # Set appropriate axis limits with more space for annotations
    if supports:
        x_margin = (max(supports) - min(supports)) * 0.15 or 5
        y_margin = (max(confidences) - min(confidences)) * 0.1 or 0.05
        ax.set_xlim(min(supports) - x_margin, max(supports) + x_margin * 3)
        ax.set_ylim(max(0, min(confidences) - y_margin), min(1, max(confidences) + y_margin))
    
    # Create figures directory if it doesn't exist
    figures_dir = "../figures"
    os.makedirs(figures_dir, exist_ok=True)
    
    # Save figure
    figure_file = f"{figures_dir}/figure_{figure_num}_rules.png"
    plt.tight_layout()
    plt.savefig(figure_file, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"\n{'='*80}")
    print(f"FIGURE {figure_num}: {title}")
    print(f"{'='*80}")
    print(f"Total rules: {len(list_setOf_rule)}")
    print(f"Figure saved to: {figure_file}")
    
    # Print decoded rules to terminal with dependency information
    print(f"\nDecoded Rules with Dependencies:")
    print("-" * 80)
    
    rules_sorted = [(lhs, rhs, supp, conf) for lhs, rhs, supp, conf in list_setOf_rule]
    rules_sorted.sort(key=lambda x: (x[3], x[2]), reverse=True)  # Sort by confidence, then support
    
    for i, (LHS, RHS, supp, conf) in enumerate(rules_sorted, 1):
        decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        
        print(f"\n{'='*80}")
        print(f"Rule {i}:")
        print(f"  Antecedent (IF): {decoded_LHS}")
        print(f"  Consequent (THEN): {decoded_RHS}")
        relative_supp = supp / len(Xbasket)
        print(f"  Support: {relative_supp:.4f} (absolute: {supp}), Confidence: {conf:.4f}")
        
        # Show dependency type
        if len(decoded_LHS) == 1 and len(decoded_RHS) == 1:
            print(f"  Type: Simple dependency (1→1)")
        elif len(decoded_LHS) > 1 and len(decoded_RHS) == 1:
            print(f"  Type: Multiple antecedents → Single consequent ({len(decoded_LHS)}→1)")
            print(f"  Interpretation: Viewing ALL of {decoded_LHS} together implies viewing {decoded_RHS[0]}")
        elif len(decoded_LHS) == 1 and len(decoded_RHS) > 1:
            print(f"  Type: Single antecedent → Multiple consequents (1→{len(decoded_RHS)})")
            print(f"  Interpretation: Viewing {decoded_LHS[0]} implies viewing ALL of {decoded_RHS}")
        else:
            print(f"  Type: Complex dependency ({len(decoded_LHS)}→{len(decoded_RHS)})")
            print(f"  Interpretation: Viewing combination {decoded_LHS} implies viewing {decoded_RHS}")
        
        # Confidence interpretation
        if conf == 1.0:
            print(f"  Strength: PERFECT (100%) - Always occurs together")
        elif conf >= 0.95:
            print(f"  Strength: VERY STRONG (≥95%) - Almost always together")
        elif conf >= 0.80:
            print(f"  Strength: STRONG (≥80%) - Frequently together")
        else:
            print(f"  Strength: MODERATE (<80%) - Sometimes together")
    
    print("=" * 80)


def find_optimal_config(X, support_range, confidence_range, config_name):
    """
    Search for optimal configuration using grid search.
    
    Args:
        X: OneHot encoded dataset
        support_range: List of support values to test
        confidence_range: List of confidence values to test
        config_name: Name of the configuration
    
    Returns:
        Tuple of (best_support, best_confidence, num_rules)
    """
    print(f"\n{config_name}: Searching optimal configuration...")
    print(f"Testing {len(support_range)} support × {len(confidence_range)} confidence = {len(support_range) * len(confidence_range)} combinations")
    
    best_config = None
    best_score = float('inf')
    
    for support_pct in support_range:
        for confidence in confidence_range:
            _, rules = generate_rules_with_config(X, support_pct, confidence)
            num_rules = len(rules)
            
            # Score: prefer configurations with rules <= TARGET_RULES_MAX, closest to max
            if num_rules <= TARGET_RULES_MAX:
                score = TARGET_RULES_MAX - num_rules  # Prefer more rules up to max
            else:
                score = 1000 + (num_rules - TARGET_RULES_MAX) * 5  # Penalize exceeding max
            
            if best_config is None or score < best_score:
                best_score = score
                best_config = (support_pct, confidence, num_rules)
    
    if best_config:
        support_pct, confidence, num_rules = best_config
        min_support = int(len(X) * support_pct)
        print(f"✓ Optimal: Support={support_pct:.2%} ({min_support} trans), Confidence={confidence:.2%}, {num_rules} rules")
        return best_config
    
    return None


def generate_all_figures(Xbasket, X, mapping):
    """
    Generate three figures for the three business questions using grid search.
    Uses grid search to find optimal parameters for each configuration.
    
    Args:
        Xbasket: Original basket dataset
        X: OneHot encoded dataset
        mapping: Encoding mapping
    """
    
    # Configuration 1: Which products should be kept together?
    # Strategy: Moderate support + good confidence (general associations)
    print("\nConfiguration 1: Products to keep together...")
    print("Strategy: Moderate support + good confidence")
    
    config_1 = find_optimal_config(X, SUPPORT_RANGE_CONFIG_1, CONFIDENCE_RANGE_CONFIG_1, "Config 1")
    if config_1:
        support_1, confidence_1, _ = config_1
        itemsets_1, rules_1 = generate_rules_with_config(X, support_1, confidence_1)
        min_support_1 = int(len(X) * support_1)
        
        plot_association_rules(
            rules_1, Xbasket, mapping,
            f"Q1: Products to Keep Together (Support≥{min_support_1}, Conf≥{int(confidence_1*100)}%)",
            1
        )
    
    # Configuration 2: Which products are rarely visited but often together?
    # Strategy: Low support + very high confidence (rare but strong associations)
    print("\n\nConfiguration 2: Rarely visited but often together...")
    print("Strategy: Low support + very high confidence")
    
    config_2 = find_optimal_config(X, SUPPORT_RANGE_CONFIG_2, CONFIDENCE_RANGE_CONFIG_2, "Config 2")
    if config_2:
        support_2, confidence_2, _ = config_2
        itemsets_2, rules_2 = generate_rules_with_config(X, support_2, confidence_2)
        min_support_2 = int(len(X) * support_2)
        
        plot_association_rules(
            rules_2, Xbasket, mapping,
            f"Q2: Rare but Strong Associations (Support≥{min_support_2}, Conf≥{int(confidence_2*100)}%)",
            2
        )
    
    # Configuration 3: Which products are the most visited?
    # Strategy: High support (most frequent) + moderate confidence
    print("\n\nConfiguration 3: Most visited products...")
    print("Strategy: High support + moderate confidence")
    
    config_3 = find_optimal_config(X, SUPPORT_RANGE_CONFIG_3, CONFIDENCE_RANGE_CONFIG_3, "Config 3")
    if config_3:
        support_3, confidence_3, _ = config_3
        itemsets_3, rules_3 = generate_rules_with_config(X, support_3, confidence_3)
        min_support_3 = int(len(X) * support_3)
        
        plot_association_rules(
            rules_3, Xbasket, mapping,
            f"Q3: Most Visited Products (Support≥{min_support_3}, Conf≥{int(confidence_3*100)}%)",
            3
        )
    
    print("\n" + "=" * 80)
    print("ALL FIGURES GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nSummary:")
    if config_1:
        support_1, confidence_1, num_rules_1 = config_1
        min_support_1 = int(len(X) * support_1)
        print(f"  Configuration 1 (Figure 1): {num_rules_1} rules [Support≥{min_support_1}, Conf≥{int(confidence_1*100)}%]")
    if config_2:
        support_2, confidence_2, num_rules_2 = config_2
        min_support_2 = int(len(X) * support_2)
        print(f"  Configuration 2 (Figure 2): {num_rules_2} rules [Support≥{min_support_2}, Conf≥{int(confidence_2*100)}%]")
    if config_3:
        support_3, confidence_3, num_rules_3 = config_3
        min_support_3 = int(len(X) * support_3)
        print(f"  Configuration 3 (Figure 3): {num_rules_3} rules [Support≥{min_support_3}, Conf≥{int(confidence_3*100)}%]")
    print(f"\nAll figures saved to PROJECT_B/figures/ directory")


def save_results_to_file(Xbasket, mapping, support_pct, confidence, min_support,
                         dict_setOf_itemset, list_setOf_rule, output_file):
    """
    Save analysis results to a text file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("EXERCISE 7 - ASSOCIATION RULES ANALYSIS\n")
        f.write("We-Commerce Market-Basket Analysis\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Configuration:\n")
        f.write(f"  Support: {support_pct:.2%} ({min_support} transactions)\n")
        f.write(f"  Confidence: {confidence:.2%}\n")
        f.write(f"  Total transactions: {len(Xbasket)}\n")
        f.write(f"  Number of rules: {len(list_setOf_rule)}\n")
        f.write(f"  Number of frequent itemsets: {len(dict_setOf_itemset)}\n\n")
        
        # Most visited products
        f.write("=" * 80 + "\n")
        f.write("1. MOST VISITED PRODUCTS\n")
        f.write("=" * 80 + "\n")
        single_items = [(itemset, supp) for itemset, supp in dict_setOf_itemset.items() 
                        if len(itemset) == 1]
        single_items.sort(key=lambda x: x[1], reverse=True)
        
        for i, (itemset, supp) in enumerate(single_items, 1):
            decoded = [var.name for _, var, _ in OneHot.decode(itemset, Xbasket, mapping)]
            support_pct_item = (supp / len(Xbasket)) * 100
            relative_supp = supp / len(Xbasket)
            f.write(f"\n{i}. {decoded[0]}\n")
            f.write(f"   Support: {relative_supp:.4f} ({support_pct_item:.2f}% of transactions, {supp} total)\n")
        
        # Association rules
        f.write("\n" + "=" * 80 + "\n")
        f.write("2. ASSOCIATION RULES (SORTED BY CONFIDENCE)\n")
        f.write("=" * 80 + "\n")
        
        rules_sorted = [(lhs, rhs, supp, conf) for lhs, rhs, supp, conf in list_setOf_rule]
        rules_sorted.sort(key=lambda x: (x[3], x[2]), reverse=True)
        
        for i, (LHS, RHS, supp, conf) in enumerate(rules_sorted, 1):
            decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
            decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
            support_pct_rule = (supp / len(Xbasket)) * 100
            relative_supp_rule = supp / len(Xbasket)
            
            f.write(f"\nRule {i}:\n")
            f.write(f"  IF: {decoded_LHS}\n")
            f.write(f"  THEN: {decoded_RHS}\n")
            f.write(f"  Support: {relative_supp_rule:.4f} ({support_pct_rule:.2f}% of transactions, {supp} total)\n")
            f.write(f"  Confidence: {conf:.2%}\n")
    
    print(f"\nResults saved to: {output_file}")


def main():
    """
    Main function to implement Exercise 7.
    Uses grid search to find optimal configurations.
    """
    print("\n" + "=" * 80)
    print("EXERCISE 7 - ASSOCIATION RULES ANALYSIS")
    print("Market-Basket Analysis for We-Commerce")
    print("=" * 80)
    print("Generating three configurations to answer business questions:")
    print("  1. Which products should be kept together?")
    print("  2. Which products are rarely visited but often together?")
    print("  3. Which products are most visited?")
    print("=" * 80 + "\n")
    print("Using GRID SEARCH to find optimal configurations.")
    print(f"Target: Maximum {TARGET_RULES_MAX} rules per configuration.\n")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if basket file exists
    if not os.path.exists(BASKET_FILE):
        print(f"ERROR: Basket file not found: {BASKET_FILE}")
        print("Please run Exercise 6 first to generate the basket file.")
        sys.exit(1)
    
    # Load dataset
    print(f"Loading dataset: {BASKET_FILE}")
    try:
        Xbasket = Orange.data.Table(BASKET_FILE)
        print(f"✓ Dataset loaded: {len(Xbasket)} transactions")
    except Exception as e:
        print(f"ERROR loading dataset: {str(e)}")
        sys.exit(1)
    
    # OneHot encoding
    print("Encoding dataset...")
    X, mapping = OneHot.encode(Xbasket)
    print(f"✓ Dataset encoded")
    
    # Generate figures for three business questions
    print("\n" + "=" * 80)
    print("GENERATING FIGURES")
    print("=" * 80)
    generate_all_figures(Xbasket, X, mapping)
    
    print("\n" + "=" * 80)
    print("EXERCISE 7 COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nThree configurations analyzed:")
    print(f"  ✓ Configuration 1: General product associations")
    print(f"  ✓ Configuration 2: Rare but strong co-visitations")
    print(f"  ✓ Configuration 3: Most visited products")
    print(f"\nAll figures saved to figures/ directory")


if __name__ == "__main__":
    main()
