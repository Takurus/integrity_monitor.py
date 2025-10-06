🐍 Python File Integrity Monitor
This project is a foundational cybersecurity tool written in Python that monitors a target directory for unauthorized changes. It uses cryptographic hashing to establish a baseline of files and alerts the user if any files have been modified, deleted, or added since the last trusted run.

🛡️ Core Security Concept
File Integrity Monitoring (FIM) is a critical security control used to detect unauthorized modifications to critical system files or configuration settings. Any change in a file's content will result in a completely different hash value, immediately alerting the user to potential tampering, malware infection, or accidental system changes.

🚀 Getting Started
Prerequisites
This project uses standard Python libraries only. You only need:

Python 3.6+ installed on your system.

Installation
No installation is required beyond downloading the script.

Save the Python code as integrity_monitor.py.

Ensure you have read/write permissions in the directory where you save the script.

💻 How to Use the Monitor
1. Establish the Baseline (First Run)
The first time you run the script, it scans the monitored_data directory and creates a trusted baseline file (integrity_baseline.json).

Create a folder named monitored_data in the same directory as the script.

Place the files you want to monitor inside monitored_data.

Run the script:

python integrity_monitor.py

Output: The script will confirm that a new baseline has been saved.

2. Check Integrity (Subsequent Runs)
After the baseline is established, every time you run the script, it performs a comparison check:

Run the script again:

python integrity_monitor.py

The monitor will compare the current state of files against the stored baseline and report on:

[ALERT - MODIFIED]: The file's hash has changed (content was altered).

[ALERT - DELETED]: The file is in the baseline but missing from the directory.

[ALERT - ADDED]: The file is new and not in the baseline.

3. Updating the Baseline
If the script detects changes, you will be prompted to update the baseline. Only update the baseline if you manually approve and trust the changes.

Do you want to update the baseline to reflect these changes? (y/N): 

Type y and Enter: The integrity_baseline.json file is overwritten with the current state.

Type N or Enter: The baseline remains unchanged, and the script will continue to flag the same changes on future runs.

⚙️ Configuration
You can easily adjust the primary settings at the top of the integrity_monitor.py file:

Constant

Description

Default Value

TARGET_DIR

The name of the folder the monitor will scan.

'monitored_data'

BASELINE_FILE

The name of the JSON file used to store the trusted hashes.

'integrity_baseline.json'

HASH_ALGORITHM

The cryptographic algorithm used to generate file fingerprints.

'sha256'

Note: You can change the HASH_ALGORITHM to 'md5', 'sha512', etc., but SHA-256 is recommended for better security.
