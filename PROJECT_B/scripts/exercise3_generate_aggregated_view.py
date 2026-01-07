#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 3: Generate Aggregated View of Data Distribution
Executes the SQL scripts via shell/batch scripts
"""

import subprocess
import sys
import os
import platform

def run_shell_script(script_name, description, script_dir):
    """
    Execute a shell/batch script that runs SQL statements.
    
    Args:
        script_name: Name of the script (e.g., "_go00.sh")
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
    Main function to execute Exercise 3.
    """
    print("\n" + "="*80)
    print("EXERCISE 3: Aggregated View of Data Distribution")
    print("="*80)
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    print(f"\nProject directory: {project_dir}")
    print(f"Script directory: {script_dir}")
    
    # Define the scripts to execute
    scripts = [
        ("_go00.sh", "Step 1: Creating database"),
        ("_go01.sh", "Step 2: Creating schema"),
        ("_go02.sh", "Step 3: Importing data from CSV"),
        ("_go03.sh", "Step 4: Creating views and generating aggregated statistics")
    ]
    
    # Execute each script
    for script_name, description in scripts:
        if not run_shell_script(script_name, description, script_dir):
            print(f"\nFailed at step: {script_name}")
            sys.exit(1)
    
    print("\n" + "="*80)
    print("EXERCISE 3 COMPLETED SUCCESSFULLY!")
    print("="*80)
    print(f"Compare with validation file: {project_dir}/z01_aggregatedView.txt")
    print()

if __name__ == "__main__":
    main()
