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

# Support range to explore (percentage of total transactions)
SUPPORT_RANGE = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01,
                 0.012, 0.015, 0.018, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]

# Confidence range to explore
CONFIDENCE_RANGE = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]


def explore_support_confidence_space(Xbasket, X, mapping, maxR):
    """
    Explore different combinations of support and confidence to find 
    configurations that produce at most maxR association rules.
    
    Args:
        Xbasket: Original basket dataset
        X: OneHot encoded dataset
        mapping: Encoding mapping
        maxR: Maximum number of rules desired
    
    Returns:
        List of (support, confidence, num_rules) tuples sorted by proximity to maxR
    """
    print(f"\nExploring support/confidence space for maxR={maxR} rules...")
    print("=" * 80)
    
    results = []
    total_transactions = len(Xbasket)
    
    for support_pct in SUPPORT_RANGE:
        min_support = max(2, int(total_transactions * support_pct))
        
        # Find frequent itemsets for this support
        try:
            setOf_itemset = frequent_itemsets(X, min_support)
            dict_setOf_itemset = dict(setOf_itemset)
            
            if len(dict_setOf_itemset) == 0:
                # No frequent itemsets, skip confidence exploration
                continue
            
            for confidence in CONFIDENCE_RANGE:
                # Generate association rules
                setOf_itemset = frequent_itemsets(X, min_support)
                dict_setOf_itemset = dict(setOf_itemset)
                setOf_rule = association_rules(dict_setOf_itemset, confidence)
                list_setOf_rule = list(setOf_rule)
                num_rules = len(list_setOf_rule)
                
                results.append((support_pct, confidence, num_rules, min_support, dict_setOf_itemset, list_setOf_rule))
                
                print(f"Support={support_pct:.2%} ({min_support} trans), Confidence={confidence:.2%} -> {num_rules} rules")
                
        except Exception as e:
            print(f"Error with support={support_pct:.2%}: {str(e)}")
            continue
    
    # Sort by proximity to maxR (prefer configurations with rules <= maxR)
    results.sort(key=lambda x: abs(x[2] - maxR) if x[2] <= maxR else x[2] + 1000)
    
    return results


def analyze_best_configuration(Xbasket, mapping, support_pct, confidence, min_support, 
                                dict_setOf_itemset, list_setOf_rule):
    """
    Analyze the best configuration found and provide marketing insights.
    
    Args:
        Xbasket: Original basket dataset
        mapping: Encoding mapping
        support_pct: Support percentage
        confidence: Confidence threshold
        min_support: Absolute minimum support
        dict_setOf_itemset: Dictionary of frequent itemsets
        list_setOf_rule: List of association rules
    """
    print("\n" + "=" * 80)
    print("BEST CONFIGURATION ANALYSIS")
    print("=" * 80)
    print(f"Support: {support_pct:.2%} ({min_support} transactions)")
    print(f"Confidence: {confidence:.2%}")
    print(f"Number of rules: {len(list_setOf_rule)}")
    print(f"Number of frequent itemsets: {len(dict_setOf_itemset)}")
    print("=" * 80)
    
    # 1. Most visited products (highest support itemsets of size 1)
    print("\n--- MOST VISITED PRODUCTS ---")
    print("(Products with highest individual support)")
    single_items = [(itemset, supp) for itemset, supp in dict_setOf_itemset.items() 
                    if len(itemset) == 1]
    single_items.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 10 most visited products:")
    for i, (itemset, supp) in enumerate(single_items[:10], 1):
        decoded = [var.name for _, var, _ in OneHot.decode(itemset, Xbasket, mapping)]
        support_pct_item = (supp / len(Xbasket)) * 100
        print(f"{i:2d}. {decoded[0]}")
        print(f"    Support: {supp} transactions ({support_pct_item:.2f}%)")
    
    # 2. Rarely visited but often co-visited products
    print("\n--- RARELY VISITED BUT OFTEN CO-VISITED ---")
    print("(Product pairs with low individual support but high confidence)")
    rare_covisited = []
    
    for LHS, RHS, supp, conf in list_setOf_rule:
        # Get individual supports for LHS and RHS items
        lhs_items = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        rhs_items = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        
        # Calculate average individual support
        combined_itemset = LHS | RHS
        combined_supp = dict_setOf_itemset.get(combined_itemset, 0)
        
        # If confidence is high but combined support is relatively low
        if conf >= 0.70 and combined_supp < min_support * 3:
            rare_covisited.append((lhs_items, rhs_items, supp, conf, combined_supp))
    
    rare_covisited.sort(key=lambda x: x[3], reverse=True)  # Sort by confidence
    
    if rare_covisited:
        print(f"\nTop 10 rarely visited but co-visited patterns:")
        for i, (lhs, rhs, supp, conf, combined_supp) in enumerate(rare_covisited[:10], 1):
            print(f"{i:2d}. {lhs} -> {rhs}")
            print(f"    Confidence: {conf:.2%}, Support: {supp} ({(supp/len(Xbasket))*100:.2f}%)")
    else:
        print("  No rare but co-visited patterns found with current criteria.")
    
    # 3. Products that should be kept together (strong association rules)
    print("\n--- PRODUCTS TO KEEP TOGETHER ON WEB PAGE ---")
    print("(Strongest association rules for cross-selling)")
    
    strong_associations = [(lhs, rhs, supp, conf) for lhs, rhs, supp, conf in list_setOf_rule]
    strong_associations.sort(key=lambda x: (x[3], x[2]), reverse=True)  # Sort by confidence, then support
    
    print(f"\nTop 15 strongest associations for product placement:")
    for i, (LHS, RHS, supp, conf) in enumerate(strong_associations[:15], 1):
        decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        support_pct_rule = (supp / len(Xbasket)) * 100
        
        print(f"\n{i:2d}. IF customer views: {decoded_LHS}")
        print(f"    THEN also show: {decoded_RHS}")
        print(f"    Confidence: {conf:.2%}, Support: {supp} ({support_pct_rule:.2f}%)")
        
        # Marketing interpretation
        if conf >= 0.90:
            print(f"    💡 STRONG: Place together - 9 out of 10 visitors will see both!")
        elif conf >= 0.75:
            print(f"    💡 GOOD: Recommend on same page - 3 out of 4 visitors interested")
        else:
            print(f"    💡 MODERATE: Consider for cross-selling campaigns")
    
    # 4. All rules summary
    print("\n" + "=" * 80)
    print("COMPLETE RULES LIST")
    print("=" * 80)
    
    for i, (LHS, RHS, supp, conf) in enumerate(strong_associations, 1):
        decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        support_pct_rule = (supp / len(Xbasket)) * 100
        
        print(f"\nRule {i}:")
        print(f"  {decoded_LHS} -> {decoded_RHS}")
        print(f"  Support: {supp} ({support_pct_rule:.2f}%), Confidence: {conf:.2%}")


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
            f.write(f"\n{i}. {decoded[0]}\n")
            f.write(f"   Support: {supp} transactions ({support_pct_item:.2f}%)\n")
        
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
            
            f.write(f"\nRule {i}:\n")
            f.write(f"  IF: {decoded_LHS}\n")
            f.write(f"  THEN: {decoded_RHS}\n")
            f.write(f"  Support: {supp} ({support_pct_rule:.2f}%)\n")
            f.write(f"  Confidence: {conf:.2%}\n")
    
    print(f"\nResults saved to: {output_file}")


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
        supports.append(supp)
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
    
    ax.set_xlabel('Support (absolute count)', fontsize=12, fontweight='bold')
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
        print(f"  Support: {supp}, Confidence: {conf:.4f}")
        
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


def generate_all_figures(Xbasket, X, mapping, maxR=10):
    """
    Generate all three figures based on different configurations.
    Uses maxR parameter to search for appropriate support/confidence combinations.
    
    Args:
        Xbasket: Original basket dataset
        X: OneHot encoded dataset
        mapping: Encoding mapping
        maxR: Target maximum number of rules for each configuration
    """
    print("\n" + "=" * 80)
    print("GENERATING FIGURES FOR DIFFERENT CONFIGURATIONS")
    print(f"Target: ~{maxR} rules per configuration")
    print("=" * 80)
    
    # Configuration 1: Which few products should be kept together in a Web page?
    # Strategy: Moderate-high support (frequently co-occurring) + moderate-high confidence
    print("\n\nConfiguration 1: Products to keep together on Web page...")
    print("Strategy: Moderate-high support + moderate-high confidence")
    
    results_1 = explore_support_confidence_space(Xbasket, X, mapping, maxR)
    # Filter for moderate-high support (>0.3%) and moderate-high confidence (>60%)
    results_1 = [r for r in results_1 if r[0] >= 0.003 and r[1] >= 0.60]
    
    if results_1:
        support_pct_1, confidence_1, num_rules_1, min_support_1, itemsets_1, rules_1 = results_1[0]
        print(f"✓ Found configuration: Support={support_pct_1:.2%} ({min_support_1} trans), Confidence={confidence_1:.2%}, {num_rules_1} rules")
        
        plot_association_rules(
            rules_1, Xbasket, mapping,
            f"Q1: Products to Keep Together (Support≥{min_support_1}, Conf≥{int(confidence_1*100)}%)",
            1
        )
    else:
        print("WARNING: No suitable configuration found for Configuration 1")
    
    # Configuration 2: Which products are rarely visited but often visited together?
    # Strategy: Low support (rare) + very high confidence (strong association)
    print("\n\nConfiguration 2: Rarely visited but often together...")
    print("Strategy: Low support + very high confidence")
    
    results_2 = explore_support_confidence_space(Xbasket, X, mapping, maxR)
    # Filter for low support (<0.3%) and very high confidence (>85%)
    results_2 = [r for r in results_2 if r[0] < 0.003 and r[1] >= 0.85]
    
    if results_2:
        support_pct_2, confidence_2, num_rules_2, min_support_2, itemsets_2, rules_2 = results_2[0]
        print(f"✓ Found configuration: Support={support_pct_2:.2%} ({min_support_2} trans), Confidence={confidence_2:.2%}, {num_rules_2} rules")
        
        plot_association_rules(
            rules_2, Xbasket, mapping,
            f"Q2: Rare but Strong Associations (Support≥{min_support_2}, Conf≥{int(confidence_2*100)}%)",
            2
        )
    else:
        print("WARNING: No suitable configuration found for Configuration 2")
    
    # Configuration 3: Which products are the most visited?
    # Strategy: High support (most frequent) + low confidence (focus on frequency)
    print("\n\nConfiguration 3: Most visited products...")
    print("Strategy: High support + low confidence")
    
    results_3 = explore_support_confidence_space(Xbasket, X, mapping, maxR)
    # Filter for high support (>0.5%) and lower confidence (50-70%)
    results_3 = [r for r in results_3 if r[0] >= 0.005 and r[1] <= 0.70]
    
    if results_3:
        support_pct_3, confidence_3, num_rules_3, min_support_3, itemsets_3, rules_3 = results_3[0]
        print(f"✓ Found configuration: Support={support_pct_3:.2%} ({min_support_3} trans), Confidence={confidence_3:.2%}, {num_rules_3} rules")
        
        plot_association_rules(
            rules_3, Xbasket, mapping,
            f"Q3: Most Visited Products (Support≥{min_support_3}, Conf≥{int(confidence_3*100)}%)",
            3
        )
    else:
        print("WARNING: No suitable configuration found for Configuration 3")
    
    print("\n" + "=" * 80)
    print("ALL FIGURES GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nSummary:")
    if results_1:
        print(f"  Configuration 1 (Figure 1): {num_rules_1} rules [Support≥{min_support_1}, Conf≥{int(confidence_1*100)}%]")
    if results_2:
        print(f"  Configuration 2 (Figure 2): {num_rules_2} rules [Support≥{min_support_2}, Conf≥{int(confidence_2*100)}%]")
    if results_3:
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
            f.write(f"\n{i}. {decoded[0]}\n")
            f.write(f"   Support: {supp} transactions ({support_pct_item:.2f}%)\n")
        
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
            
            f.write(f"\nRule {i}:\n")
            f.write(f"  IF: {decoded_LHS}\n")
            f.write(f"  THEN: {decoded_RHS}\n")
            f.write(f"  Support: {supp} ({support_pct_rule:.2f}%)\n")
            f.write(f"  Confidence: {conf:.2%}\n")
    
    print(f"\nResults saved to: {output_file}")


def main():
    """
    Main function to implement Exercise 7.
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
    
    # Parse command-line arguments
    maxR = 10  # Default target number of rules
    if len(sys.argv) > 1:
        try:
            maxR = int(sys.argv[1])
            print(f"Using maxR={maxR} (target number of rules per configuration)")
        except ValueError:
            print(f"WARNING: Invalid maxR value '{sys.argv[1]}', using default maxR=10")
    else:
        print(f"Using default maxR={maxR} (target number of rules per configuration)")
        print(f"Usage: python3.10 {os.path.basename(__file__)} [maxR]")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if basket file exists
    if not os.path.exists(BASKET_FILE):
        print(f"ERROR: Basket file not found: {BASKET_FILE}")
        print("Please run Exercise 6 first to generate the basket file.")
        sys.exit(1)
    
    # Load dataset
    print(f"\nLoading dataset: {BASKET_FILE}")
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
    generate_all_figures(Xbasket, X, mapping, maxR)
    
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
