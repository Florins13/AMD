#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 6: Transform Transactions to Basket Format
Based on PRACTICE_7 _goPy_transform_v02.py
Author: Paulo Trigo Silva (PTS) - Adapted for PROJECT_B
"""

import csv
import unicodedata
import sys
import os


def remove_accents(aString, encoding='utf-8'):
    """
    Remove accents from unicode string.
    """
    aString_unicode = aString
    nfkd_form = unicodedata.normalize('NFKD', aString_unicode)
    only_ascii_form = nfkd_form.encode('ascii', 'ignore').decode(encoding)
    return only_ascii_form


def normalizeString(aString):
    """
    Normalize product strings for basket analysis:
    - Replace "=" with "+" (= is used in basket format)
    - Eliminate white spaces
    - Eliminate quotes
    - Remove accent characters
    - Convert to lowercase
    """
    # substitute "=" symbol because it is used in the basket format
    aString = aString.replace("=", "+")
    
    # eliminate spaces (white characters)
    aString = aString.replace(" ", "")
    
    # eliminate quotes (" character)
    aString = aString.replace("\"", "$")
    
    # eliminate accent characters
    encoding_windows = "iso-8859-1"
    aString = remove_accents(aString, encoding_windows)
    
    # to lower case
    aString = aString.lower()
    
    return aString


def generateBasket(fileNameIN):
    """
    Generate basket structure from CSV file with format:
    TransactionID;ProductID
    
    Returns:
        basket: dict of transactions with item counts
        all_itemset: dict of all unique items with index
    """
    indexTransaction = 0
    indexItem = 1
    basket = {}
    all_itemset = {}
    len_itemset = 0
    
    print(f"Reading file: {fileNameIN}")
    
    with open(fileNameIN, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        
        for row in reader:
            transactionID = row[indexTransaction]
            
            if transactionID not in basket:
                basket[transactionID] = {}
            
            itemID = row[indexItem]
            itemID = normalizeString(str(itemID))
            
            if itemID not in basket[transactionID]:
                basket[transactionID][itemID] = 0
            basket[transactionID][itemID] += 1
            
            # build an itemset with all items
            # each item is associated with an order relation (len_itemset)
            if itemID not in all_itemset:
                all_itemset[itemID] = len_itemset
                len_itemset += 1
    
    print(f"  Transactions loaded: {len(basket)}")
    print(f"  Unique items: {len(all_itemset)}")
    
    return (basket, all_itemset)


def generateDataFile_basket(basket, fileNameOUT):
    """
    Generate .basket file for Orange (space-separated items per line).
    """
    print(f"Generating: {fileNameOUT}")
    
    with open(fileNameOUT, mode='wt', encoding='utf-8') as f:
        for transactionID in basket:
            line = ""
            for itemID in basket[transactionID]:
                if line != "":
                    line += " "
                line += itemID
            f.write(line + '\n')
    
    print(f"  ✓ Basket file created with {len(basket)} transactions")


def generateDataFile_tab(basket, all_itemset, fileNameOUT):
    """
    Generate .tab file for Orange (tab-separated matrix format).
    """
    print(f"Generating: {fileNameOUT}")
    
    all_itemset_list = [k for k in sorted(all_itemset, key=all_itemset.get)]
    all_transactionID_list = list(basket.keys())
    all_transactionID_list.sort()
    
    with open(fileNameOUT, mode='wt', encoding='utf-8') as f:
        # Header line: item names
        line = ""
        for itemName in all_itemset_list:
            if line != "":
                line += "\t"
            line += str(itemName)
        f.write(line + '\n')
        
        # Type line: all discrete
        line = ""
        for _ in all_itemset_list:
            if line != "":
                line += "\t"
            line += str("d")
        f.write(line + '\n')
        
        # Flags line: empty
        line = ""
        len_itemset_list = len(all_itemset_list)
        for n in range(len_itemset_list):
            if n < len_itemset_list - 1:
                line += "\t"
        f.write(line + '\n')
        
        # Data lines: transaction rows
        for transactionID in all_transactionID_list:
            line_list = [0] * len_itemset_list
            for itemID in basket[transactionID]:
                itemID_index = all_itemset[itemID]
                line_list[itemID_index] = basket[transactionID][itemID]
            
            line = ""
            for number in line_list:
                if line != "":
                    line += "\t"
                line += str(number)
            f.write(line + '\n')
    
    print(f"  ✓ Tab file created with {len(basket)} rows x {len(all_itemset)} columns")


def main():
    """
    Main function for Exercise 6.
    """
    print("\n" + "="*80)
    print("EXERCISE 6: Transform Transactions to Basket Format")
    print("="*80)
    print()
    
    # Get script directory and change to PROJECT_B root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    # Input and output files
    fIN = "transactions_filtered.txt"
    fOUT = "transactions_basket"
    
    if not os.path.exists(fIN):
        print(f"ERROR: Input file not found: {fIN}")
        print("Please run Exercise 5 first to generate the transactions file.")
        sys.exit(1)
    
    # Step 1: Generate basket structure
    print("Step 1: Generate Basket structure from CSV file")
    print("-" * 80)
    (basket, all_itemset) = generateBasket(fIN)
    print()
    
    # Step 2: Generate .basket file
    print("Step 2: Generate .basket dataset file")
    print("-" * 80)
    fOUT_basket = fOUT + ".basket"
    generateDataFile_basket(basket, fOUT_basket)
    print()
    
    # Step 3: Generate .tab file
    print("Step 3: Generate .tab dataset file")
    print("-" * 80)
    fOUT_tab = fOUT + ".tab"
    generateDataFile_tab(basket, all_itemset, fOUT_tab)
    print()
    
    print("="*80)
    print("EXERCISE 6 COMPLETED SUCCESSFULLY!")
    print("="*80)
    print(f"\nOutput files:")
    print(f"  - {fOUT_basket} (Orange basket format)")
    print(f"  - {fOUT_tab} (Orange tab format)")
    print(f"\nThese files can now be used in Orange for market-basket analysis.")
    print()


if __name__ == "__main__":
    main()
