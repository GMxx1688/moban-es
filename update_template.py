#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    print("Starting template update process...")
    
    # Make scripts executable
    os.chmod('rename_selectors.py', 0o755)
    os.chmod('add_breadcrumb.py', 0o755)
    
    # Step 1: Rename CSS selectors
    print("\n=== Step 1: Renaming CSS selectors ===")
    result = subprocess.run(['python3', 'rename_selectors.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error renaming CSS selectors:")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)
    
    # Step 2: Add breadcrumb navigation
    print("\n=== Step 2: Adding breadcrumb navigation ===")
    result = subprocess.run(['python3', 'add_breadcrumb.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error adding breadcrumb navigation:")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)
    
    print("\nTemplate update completed successfully!")
    print("CSS selectors have been renamed and breadcrumb navigation has been added.")
    print("Check selector_mapping.txt for the mapping of old to new selector names.")

if __name__ == "__main__":
    main()

