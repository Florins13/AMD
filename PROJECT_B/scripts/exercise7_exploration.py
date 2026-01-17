#!/usr/bin/env python3.10
"""
Exercise 7 - Association Rules Exploration
Systematically explores support-confidence combinations while constraining the number of rules (maxR)
Then shows detailed marketing insights for the best configurations
"""

import sys
import os
import Orange
from orangecontrib.associate.fpgrowth import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

def explore_configuration(Xbasket, X, mapping, config_name, support_values, confidence_values, maxR=10, filter_func=None):
    """
    Systematically explore support-confidence space for a configuration.
    
    Args:
        Xbasket: Original basket data
        X: OneHot encoded data
        mapping: OneHot mapping
        config_name: Name of the configuration
        support_values: List of support thresholds to test
        confidence_values: List of confidence thresholds to test
        maxR: Maximum number of rules to keep per combination
        filter_func: Optional function to filter rules (for Config 2 and 3)
    
    Returns:
        List of exploration results: [(supp, conf, rules_list, num_rules), ...]
    """
    print(f"\n{'='*80}")
    print(f"EXPLORING: {config_name}")
    print(f"Testing {len(support_values)} × {len(confidence_values)} = {len(support_values)*len(confidence_values)} combinations")
    print(f"Constraining to maxR={maxR} rules per combination")
    print(f"{'='*80}\n")
    
    total_transactions = len(Xbasket)
    exploration_results = []
    
    for supp in support_values:
        for conf in confidence_values:
            min_support = max(2, int(total_transactions * supp))
            itemsets = dict(frequent_itemsets(X, min_support))
            
            if not itemsets:
                trans_count = int(supp * total_transactions)
                print(f"Support={supp:.3f} ({trans_count:3d} trans), Confidence={conf:.2f} -> 0 rules")
                exploration_results.append((supp, conf, [], 0))
                continue
            
            rules = list(association_rules(itemsets, conf))
            
            # Apply custom filter if provided (for Config 2 and 3)
            if filter_func:
                rules = filter_func(rules)
            
            num_rules = len(rules)
            trans_count = int(supp * total_transactions)
            
            # Discard combinations that generate MORE than maxR rules
            if num_rules > maxR:
                print(f"Support={supp:.3f} ({trans_count:3d} trans), Confidence={conf:.2f} -> {num_rules:3d} rules (DISCARDED: exceeds maxR={maxR})")
                exploration_results.append((supp, conf, [], 0))
                continue
            
            print(f"Support={supp:.3f} ({trans_count:3d} trans), Confidence={conf:.2f} -> {num_rules:3d} rules")
            exploration_results.append((supp, conf, rules, num_rules))
    
    return exploration_results

def plot_exploration_results(exploration_results, config_name, figure_num):
    """
    Create scatter plot showing how support/confidence affect number of rules.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extract data for plotting
    supports = []
    confidences = []
    num_rules_list = []
    
    for supp, conf, rules, num_rules in exploration_results:
        if num_rules > 0:  # Only plot combinations that generated rules
            supports.append(supp)
            confidences.append(conf)
            num_rules_list.append(num_rules)
    
    if not supports:
        print(f"No rules to plot for {config_name}")
        return
    
    # Create scatter plot with color-coded points based on number of rules
    scatter = ax.scatter(supports, confidences, 
                        c=num_rules_list, 
                        s=200, 
                        cmap='viridis', 
                        alpha=0.7,
                        edgecolors='black',
                        linewidth=1)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Number of Rules', rotation=270, labelpad=20, fontsize=12)
    
    # Add labels for each point
    for supp, conf, num_rules in zip(supports, confidences, num_rules_list):
        ax.annotate(f'{num_rules}', 
                   (supp, conf), 
                   textcoords="offset points", 
                   xytext=(0,5), 
                   ha='center',
                   fontsize=8,
                   weight='bold')
    
    ax.set_xlabel('Support', fontsize=14, weight='bold')
    ax.set_ylabel('Confidence', fontsize=14, weight='bold')
    ax.set_title(f'Figure {figure_num}: {config_name}\nSupport-Confidence Space Exploration', 
                fontsize=16, weight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    os.makedirs('../figures', exist_ok=True)
    filename = f'../figures/figure_{figure_num}_exploration_{config_name.replace(" ", "_").lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {filename}\n")
    plt.close()

def plot_association_rules(list_setOf_rule, Xbasket, mapping, title, figure_num):
    """
    Create scatter plot of association rules (support vs confidence) with decoded product names.
    Similar to OLD implementation.
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
        
        # Create short label for the rule - shorten product names
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
        x_margin = (max(supports) - min(supports)) * 0.15 or 0.001
        y_margin = (max(confidences) - min(confidences)) * 0.1 or 0.05
        ax.set_xlim(min(supports) - x_margin, max(supports) + x_margin * 3)
        ax.set_ylim(max(0, min(confidences) - y_margin), min(1, max(confidences) + y_margin))
    
    # Save figure
    os.makedirs('../figures', exist_ok=True)
    figure_file = f"../figures/figure_{figure_num}_rules.png"
    plt.tight_layout()
    plt.savefig(figure_file, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"\n{'='*80}")
    print(f"FIGURE {figure_num}: {title}")
    print(f"{'='*80}")
    print(f"Total rules: {len(list_setOf_rule)}")
    print(f"Figure saved to: {figure_file}")
    
    # Print decoded rules in compact format (like terminal image)
    print(f"\nAssociation Rules (compact format):")
    print("-" * 80)
    
    rules_sorted = [(lhs, rhs, supp, conf) for lhs, rhs, supp, conf in list_setOf_rule]
    rules_sorted.sort(key=lambda x: (x[3], x[2]), reverse=True)  # Sort by confidence, then support
    
    for i, (LHS, RHS, supp, conf) in enumerate(rules_sorted, 1):
        decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
        decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
        
        # Print in compact format: rule: N - (support, confidence): [items] -> [items]
        print(f"rule: {i} - ({supp}, {conf}): {decoded_LHS} -> {decoded_RHS}")
    
    print("=" * 80)
    
    # Print detailed rules with marketing insights
    print(f"\nDetailed Rules with Marketing Recommendations:")
    print("-" * 80)
    
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
        
        # Confidence interpretation (marketing recommendations)
        if conf == 1.0:
            print(f"  Strength: PERFECT (100%) - Always occurs together")
        elif conf >= 0.95:
            print(f"  Strength: VERY STRONG (≥95%) - Almost always together")
        elif conf >= 0.80:
            print(f"  Strength: STRONG (≥80%) - Frequently together")
        else:
            print(f"  Strength: MODERATE (<80%) - Sometimes together")
    
    print("=" * 80)

def select_best_config_from_exploration(exploration_results, maxR, config_name):
    """
    Select the best configuration from exploration results.
    Strategy: Pick the combination closest to maxR rules that actually generated rules.
    """
    best_combo = None
    best_diff = float('inf')
    best_rules = []
    
    for supp, conf, rules, num_rules in exploration_results:
        if num_rules > 0:
            diff = abs(num_rules - maxR)
            if diff < best_diff:
                best_diff = diff
                best_combo = (supp, conf)
                best_rules = rules
    
    if best_combo:
        print(f"\n{'='*80}")
        print(f"{config_name}: BEST CONFIGURATION SELECTED")
        print(f"{'='*80}")
        print(f"Selected: Support={best_combo[0]:.4f}, Confidence={best_combo[1]:.2f}")
        print(f"Generated {len(best_rules)} rules (target was maxR={maxR})")
    
    return best_combo, best_rules

def main():
    print("="*80)
    print("EXERCISE 7 - ASSOCIATION RULES WITH EXPLORATION + DETAILED ANALYSIS")
    print("Step 1: Grid search exploration of support-confidence space")
    print("Step 2: Detailed marketing analysis of best configurations")
    print("="*80)
    
    # Load data
    print("\nLoading transactions data...")
    Xbasket = Orange.data.Table('../transactions_basket.basket')
    print(f"✓ Loaded {len(Xbasket)} transactions with {len(Xbasket.domain.attributes)} unique products")
    
    # OneHot encoding
    X, mapping = OneHot.encode(Xbasket)
    
    # Get maxR from command line or use default
    maxR = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(f"\nConstraining to maxR={maxR} rules per combination")
    
    # ============================================================================
    # CONFIGURATION 1: General Product Associations
    # Explore moderate support and confidence ranges
    # ============================================================================
    print("\n" + "="*80)
    print("CONFIGURATION 1: General Product Associations")
    print("Exploring moderate support and confidence ranges")
    print("="*80)
    
    config1_results = explore_configuration(
        Xbasket, X, mapping,
        config_name="Config 1: Products to Keep Together",
        support_values=[0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.010],
        confidence_values=[0.50, 0.60, 0.65, 0.70, 0.75, 0.80],
        maxR=maxR
    )
    plot_exploration_results(config1_results, "Config_1_Moderate", 1)
    
    # Select best and plot detailed rules
    best_combo1, best_rules1 = select_best_config_from_exploration(
        config1_results, maxR, "Configuration 1"
    )
    if best_rules1:
        plot_association_rules(
            best_rules1, 
            Xbasket, 
            mapping,
            f"Figure 1: Configuration 1 - General Product Associations (Support={best_combo1[0]:.4f}, Confidence={best_combo1[1]:.2f})",
            figure_num=1
        )
    
    # ============================================================================
    # CONFIGURATION 2: Rare but Strong Associations
    # Explore low support with high confidence
    # Filter: support < 15 transactions AND confidence >= 85%
    # ============================================================================
    print("\n" + "="*80)
    print("CONFIGURATION 2: Rare but Strong Associations")
    print("Exploring low support with very high confidence")
    print("Filter: support < 15 transactions AND confidence >= 85%")
    print("="*80)
    
    def config2_filter(rules):
        return [(lhs, rhs, s, c) for lhs, rhs, s, c in rules if s < 15 and c >= 0.85]
    
    config2_results = explore_configuration(
        Xbasket, X, mapping,
        config_name="Config 2: Rare but Strong",
        support_values=[0.001, 0.002, 0.003, 0.004, 0.005, 0.006],
        confidence_values=[0.85, 0.90, 0.95],
        maxR=maxR,
        filter_func=config2_filter
    )
    plot_exploration_results(config2_results, "Config_2_Rare_Strong", 2)
    
    # Select best and plot detailed rules
    best_combo2, best_rules2 = select_best_config_from_exploration(
        config2_results, maxR, "Configuration 2"
    )
    if best_rules2:
        plot_association_rules(
            best_rules2, 
            Xbasket, 
            mapping,
            f"Figure 2: Configuration 2 - Rare but Strong (Support={best_combo2[0]:.4f}, Confidence={best_combo2[1]:.2f})",
            figure_num=2
        )
    
    # ============================================================================
    # CONFIGURATION 3: Most Visited Products
    # Explore low support threshold, select highest support rules
    # Sort by support descending and take top maxR
    # ============================================================================
    print("\n" + "="*80)
    print("CONFIGURATION 3: Most Visited Products")
    print("Exploring patterns with highest support (most frequent)")
    print("Strategy: From all generated rules, select top maxR by support")
    print("="*80)
    
    def config3_filter(rules):
        # Sort by support (descending) and take top maxR
        return sorted(rules, key=lambda r: r[2], reverse=True)[:maxR]
    
    config3_results = explore_configuration(
        Xbasket, X, mapping,
        config_name="Config 3: Most Visited",
        support_values=[0.001, 0.002, 0.003, 0.004, 0.005, 0.007, 0.010],
        confidence_values=[0.50, 0.55, 0.60, 0.65, 0.70],
        maxR=maxR,
        filter_func=config3_filter
    )
    plot_exploration_results(config3_results, "Config_3_Most_Visited", 3)
    
    # Select best and plot detailed rules
    best_combo3, best_rules3 = select_best_config_from_exploration(
        config3_results, maxR, "Configuration 3"
    )
    if best_rules3:
        plot_association_rules(
            best_rules3, 
            Xbasket, 
            mapping,
            f"Figure 3: Configuration 3 - Most Visited Products (Support={best_combo3[0]:.4f}, Confidence={best_combo3[1]:.2f})",
            figure_num=3
        )
    
    # ============================================================================
    # FINAL SUMMARY
    # ============================================================================
    print("\n" + "="*80)
    print("EXPLORATION & ANALYSIS COMPLETE")
    print("="*80)
    
    print(f"\nConfiguration 1 tested {len(config1_results)} combinations")
    config1_with_rules = sum(1 for _, _, _, n in config1_results if n > 0)
    print(f"  → {config1_with_rules} combinations generated rules")
    if best_rules1:
        print(f"  → Best: Support={best_combo1[0]:.4f}, Confidence={best_combo1[1]:.2f} ({len(best_rules1)} rules)")
    
    print(f"\nConfiguration 2 tested {len(config2_results)} combinations")
    config2_with_rules = sum(1 for _, _, _, n in config2_results if n > 0)
    print(f"  → {config2_with_rules} combinations generated rules")
    if best_rules2:
        print(f"  → Best: Support={best_combo2[0]:.4f}, Confidence={best_combo2[1]:.2f} ({len(best_rules2)} rules)")
    
    print(f"\nConfiguration 3 tested {len(config3_results)} combinations")
    config3_with_rules = sum(1 for _, _, _, n in config3_results if n > 0)
    print(f"  → {config3_with_rules} combinations generated rules")
    if best_rules3:
        print(f"  → Best: Support={best_combo3[0]:.4f}, Confidence={best_combo3[1]:.2f} ({len(best_rules3)} rules)")
    
    print("\n✓ All figures saved to ../figures/ directory")
    print("  - Exploration heatmaps show the grid search process")
    print("  - Detailed rule plots show marketing insights for best configurations")
    print("="*80)


if __name__ == "__main__":
    main()
