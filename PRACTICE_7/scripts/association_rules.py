# -*- coding: utf-8 -*-
# ===============================
# Exercise 7b - Association Rules
# Programmatic implementation
# ===============================

import Orange
from orangecontrib.associate.fpgrowth import *
import os

SUPPORT_PERCENT = 0.25  # 25%
CONFIDENCE = 0.80       # 80%

# Dataset paths
DATASETS = [
    "../x_test_01-abstract.basket",
    "../x_test_02-supermarket.basket",
    "../x_test_03-documents.basket"
]


def process_basket_file(file_path, support_percent, confidence):
    """
    Process a basket file to find frequent itemsets and association rules.
    
    Args:
        file_path: Path to the basket file
        support_percent: Minimum support as a percentage (0-1)
        confidence: Minimum confidence (0-1)
    """
    print("=" * 80)
    print(f"Processing: {os.path.basename(file_path)}")
    print("=" * 80)
    
    # Read the dataset (basket format)
    Xbasket = Orange.data.Table(file_path)
    print(f"\nDataset loaded: {len(Xbasket)} transactions")
    
    # Calculate absolute support from percentage (minimum of 2 to avoid trivial patterns)
    min_support = max(2, int(len(Xbasket) * support_percent))
    print(f"Minimum support: {support_percent*100}% = {min_support} transactions")
    print(f"Minimum confidence: {confidence*100}%")
    
    # OneHot encoding
    X, mapping = OneHot.encode(Xbasket)
    
    # Find frequent itemsets
    print(f"\n--- Frequent Itemsets (min support = {min_support}) ---")
    setOf_itemset = frequent_itemsets(X, min_support)
    dict_setOf_itemset = dict(setOf_itemset)
    
    print(f"Number of frequent itemsets: {len(dict_setOf_itemset)}")
    
    # Decode and display itemsets
    print("\nFrequent itemsets (decoded):")
    for itemset, supp in sorted(dict_setOf_itemset.items(), key=lambda x: x[1], reverse=True):
        decoded_itemset = [var.name for _, var, _ in OneHot.decode(itemset, Xbasket, mapping)]
        support_pct = (supp / len(Xbasket)) * 100
        print(f"  {decoded_itemset} -> support: {supp} ({support_pct:.2f}%)")
    
    # Generate association rules
    print(f"\n--- Association Rules (min confidence = {confidence}) ---")
    setOf_itemset = frequent_itemsets(X, min_support)
    dict_setOf_itemset = dict(setOf_itemset)
    setOf_rule = association_rules(dict_setOf_itemset, confidence)
    list_setOf_rule = list(setOf_rule)
    
    print(f"Number of association rules: {len(list_setOf_rule)}")
    
    # Decode and display rules
    if list_setOf_rule:
        print("\nAssociation rules (decoded):")
        for LHS, RHS, supp, conf in list_setOf_rule:
            decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
            decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
            support_pct = (supp / len(Xbasket)) * 100
            print(f"  {decoded_LHS} -> {decoded_RHS}")
            print(f"    support: {supp} ({support_pct:.2f}%), confidence: {conf:.2%}")
    else:
        print("  No rules found with the specified parameters.")
    
    print()


def main():
    """
    Main function to process all datasets.
    """
    print("\n" + "=" * 80)
    print("ASSOCIATION RULES ANALYSIS - Exercise 7b")
    print("=" * 80)
    print(f"Global parameters:")
    print(f"  - Support: {SUPPORT_PERCENT*100}%")
    print(f"  - Confidence: {CONFIDENCE*100}%")
    print("=" * 80 + "\n")
    
    for dataset_path in DATASETS:
        try:
            # Change to the script directory to use relative paths
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, dataset_path)
            
            process_basket_file(full_path, SUPPORT_PERCENT, CONFIDENCE)
            
        except FileNotFoundError:
            print(f"ERROR: File not found: {dataset_path}")
            print()
        except Exception as e:
            print(f"ERROR processing {dataset_path}: {str(e)}")
            print()
    
    print("=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
