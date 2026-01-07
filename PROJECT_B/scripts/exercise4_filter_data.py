#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 4: Filter Relevant Data for Market-Basket Analysis
Executes SQL script to filter visitors with 5-30 sessions
"""

import subprocess
import sys
import os
import platform

def run_shell_script(script_name, description, script_dir):
    """
    Execute a shell/batch script that runs SQL statements.
    
    Args:
        script_name: Name of the script (e.g., "_go04.sh")
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
    Main function to execute Exercise 4.
    """
    print("\n" + "="*80)
    print("EXERCISE 4: Filter Relevant Data for Market-Basket Analysis")
    print("="*80)
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    print(f"\nProject directory: {project_dir}")
    print(f"Script directory: {script_dir}")
    print("\nFilter criteria: 5 ≤ number-of-sessions ≤ 30")
    
    # Execute the filtering script
    if not run_shell_script("_go04.sh", "Filtering data for visitors with 5-30 sessions", script_dir):
        print("\nFailed to filter data")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("EXERCISE 4 COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nFiltered view 'v_export_filtered' created in database")
    print("Contains events from visitors with 5-30 sessions")

if __name__ == "__main__":
    main()
