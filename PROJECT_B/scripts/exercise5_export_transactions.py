#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 5: Export Transactions for Market-Basket Analysis
Exports transaction data (TRANSACTION_ID;PRODUCT_ID) from filtered view
"""

import subprocess
import sys
import os
import platform

def run_shell_script(script_name, description, script_dir):
    """
    Execute a shell/batch script that runs SQL statements.
    
    Args:
        script_name: Name of the script (e.g., "_go05.sh")
        description: Description of what the script does
        script_dir: Scripts directory to run from
    """
    try:
        print(f"\n{'='*80}")
        print(f"{description}")
        print('='*80)
        
        # Choose script based on platform
        if platform.system() == "Windows":
            script_path = os.path.join("batch_scripts", script_name.replace(".sh", ".bat"))
            cmd = [script_path]
        else:
            script_path = os.path.join("shell_scripts", script_name)
            cmd = ['bash', script_path]
        
        result = subprocess.run(cmd, 
                              cwd=script_dir,
                              capture_output=True, 
                              text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)
        
        if result.returncode != 0:
            print(f"ERROR: Script {script_path} failed with return code {result.returncode}")
            return False
        
        print(f"SUCCESS: {description} completed")
        return True
        
    except Exception as e:
        print(f"ERROR executing {script_path}: {str(e)}")
        return False

def main():
    """
    Main function to execute Exercise 5.
    """
    print("\n" + "="*80)
    print("EXERCISE 5: Export Transactions for Market-Basket Analysis")
    print("="*80)
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    print(f"\nProject directory: {project_dir}")
    print(f"Script directory: {script_dir}")
    print("\nExport format: TRANSACTION_ID;PRODUCT_ID")
    print("Output file: transactions_filtered.txt")
    
    # Execute the export script
    if not run_shell_script("_go05.sh", "Exporting filtered transactions to text file", script_dir):
        print("\nFailed to export transactions")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("EXERCISE 5 COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    # Check if output file was created
    output_file = os.path.join(project_dir, "transactions_filtered.txt")
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        with open(output_file, 'r') as f:
            line_count = sum(1 for _ in f)
        print(f"\nOutput file created: transactions_filtered.txt")
        print(f"File size: {file_size:,} bytes")
        print(f"Total transactions: {line_count:,} records")
    else:
        print(f"\nWARNING: Output file not found at {output_file}")

if __name__ == "__main__":
    main()
