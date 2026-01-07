#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJECT_B - SQL Script Runner
Adapted from PRACTICE_7
"""

import os
import platform
import sys

def run_all_scripts():
    """Execute all SQL scripts in sequence for Exercise 3"""
    scripts = [
        ("00", "00_create_database.sql", "Create Database"),
        ("01", "01_create_schema.sql", "Create Schema"),
        ("02", "02_import_data.sql", "Import Data"),
        ("03", "03_create_views_exercise3.sql", "Create Views - Exercise 3"),
        ("04", "04_filter_data_exercise4.sql", "Filter Data - Exercise 4"),
        ("05", "05_export_transactions_exercise5.sql", "Export Transactions - Exercise 5")
    ]
    
    print("="*80)
    print("PROJECT_B - Exercises 3, 4 & 5: Data Analysis and Export")
    print("="*80)
    
    for script_num, script_file, description in scripts:
        print(f"\nStep {script_num}: {description}")
        print(f"Executing: {script_file}")
        print("-"*80)
        
        if platform.system() == "Windows":
            cmd = f"batch_scripts\\_go{script_num}.bat"
        else:  # Linux, macOS, Unix
            cmd = f"./shell_scripts/_go{script_num}.sh"
        
        result = os.system(cmd)
        
        if result != 0:
            print(f"\nERROR: Script {script_file} failed!")
            sys.exit(1)
        
        print(f"SUCCESS: {description} completed\n")
    
    print("="*80)
    print("All scripts executed successfully!")
    print("="*80)

if __name__ == "__main__":
    run_all_scripts()
