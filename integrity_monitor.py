import os
import hashlib
import json
import time

# --- CONFIGURATION ---
# Define the directory to monitor (use a specific folder for testing, not root)
TARGET_DIR = 'monitored_data' 
# Define the file where the known hashes will be stored (the baseline)
BASELINE_FILE = 'integrity_baseline.json' 
# The hashing algorithm to use
HASH_ALGORITHM = 'sha256' 

def calculate_hash(filepath, algorithm=HASH_ALGORITHM):
    """Calculates the hash of a given file content."""
    # Use 'with open' to ensure the file is properly closed
    try:
        hasher = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            # Read and update hash string in 64kb chunks
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        # File might have been deleted between the check and the attempt to hash
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def load_baseline():
    """Loads the stored hash baseline from the JSON file."""
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error: Baseline file is corrupted. Creating new baseline.")
                return {}
    return {}

def save_baseline(data):
    """Saves the current file hashes as the new baseline."""
    with open(BASELINE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n[+] New baseline successfully saved to {BASELINE_FILE}.")

def get_current_hashes():
    """Traverses the target directory and calculates the hash for every file."""
    current_hashes = {}
    
    # Check if the target directory exists, if not, create it for testing
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"[!] Target directory '{TARGET_DIR}' created. Please add some files and run again.")
        return {}

    print(f"[*] Scanning files in '{TARGET_DIR}'...")
    
    # os.walk is used to traverse directories recursively
    for root, _, files in os.walk(TARGET_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Store the path relative to the target directory
            relative_path = os.path.relpath(filepath, TARGET_DIR)
            file_hash = calculate_hash(filepath)
            
            if file_hash:
                current_hashes[relative_path] = file_hash
    
    return current_hashes

def check_integrity():
    """Compares current file hashes against the stored baseline."""
    baseline = load_baseline()
    current = get_current_hashes()
    
    if not baseline:
        print("[!] No baseline found. Creating a new one.")
        save_baseline(current)
        return

    # Flags to track changes
    found_changes = False
    
    print("\n--- INTEGRITY CHECK RESULTS ---")

    # 1. Check for Modified or Deleted Files
    for path, old_hash in baseline.items():
        if path not in current:
            # File was deleted
            print(f"[ALERT - DELETED] File removed: {path}")
            found_changes = True
        elif current[path] != old_hash:
            # File was modified (hash changed)
            print(f"[ALERT - MODIFIED] File changed: {path}")
            print(f"    - Old Hash: {old_hash}")
            print(f"    - New Hash: {current[path]}")
            found_changes = True

    # 2. Check for Added Files
    for path in current:
        if path not in baseline:
            # New file detected
            print(f"[ALERT - ADDED] New file detected: {path}")
            found_changes = True

    if not found_changes:
        print("[SUCCESS] All monitored files are consistent with the baseline.")
    
    print("-------------------------------")
    
    # Optional: Offer to update the baseline after a successful manual inspection
    if found_changes:
        response = input("Do you want to update the baseline to reflect these changes? (y/N): ").lower()
        if response == 'y':
            save_baseline(current)
        else:
            print("[INFO] Baseline NOT updated. Continuing to monitor previous state.")


if __name__ == "__main__":
    print(f"*** Python File Integrity Monitor ***")
    print(f"Monitoring Directory: {os.path.abspath(TARGET_DIR)}")
    print(f"Baseline File: {BASELINE_FILE}\n")

    # If the database file exists, run the check. Otherwise, create the first baseline.
    if os.path.exists(BASELINE_FILE):
        check_integrity()
    else:
        current_hashes = get_current_hashes()
        if current_hashes:
            save_baseline(current_hashes)
        else:
            print(f"\n[INFO] '{TARGET_DIR}' is empty. Add files and run again to establish the baseline.")
