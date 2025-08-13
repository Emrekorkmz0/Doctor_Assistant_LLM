"""
chat regulary using fastapi from terminal (post)
api endpoint: /chat

"""

import requests

# api url

API_URL = "http://127.0.0.1:8000/chat"

name = input("Name: ")
age = input("Age: ")

print("\n Chat is started")

# create loop and get info from user

while True:
    user_msg = input(f"{name}: ")
    if user_msg.lower() =="quit":
        print("Conversation is over")
        break

    # data packet which will be sent

    payload = {
        "name":name,
        "age":age,
        "message":user_msg
    }
    try:
        # send post request to fastAPI and wait 30 second

        res = requests.post(API_URL,
                            json=payload,timeout=30)
        
        # if request is success
        if res.status_code == 200:
            print(f"Assistant: {res.json()["response"]}")
        else:
            print("Error: ",res.status_code,res.text)
        
    except requests.exceptions.RequestException as e:
        print("Connection error: ",e)

