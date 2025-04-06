import os
import io

from io import BytesIO
from flask import Flask, send_file, request
from flask_socketio import SocketIO, emit
from cryptography.fernet import Fernet
from sql import db
import requests
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

key = b'1MhGGPkq2W_M99LYLsheX6yOfn1ZFXbR2yrHp-CqOfY='
fernet = Fernet(key)

ipToPost = ("quilt.duckdns.org",)

@app.route('/')
def home():
    return open(os.path.join(ROOT, 'resources', 'index.html')).read()

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    username = data.get('username')
    password = data.get('password')

    if user_exists_in_sql(username, password) is not None:
        user_code = username + "_" + password + "_291"
        token = fernet.encrypt(user_code.encode()).decode()
        return {
            "token": token
        }, 200

    return {
        "error": "Incorrect Password"
    }, 401

@app.route('/auth/createAccout', methods=['POST'])
def create_account():
    data = request.get_json()
    print(data)
    username = data.get('username')
    password = data.get('password')
    minecraft_uuid = data.get('minecratUUID')
    discord_id = data.get('discordID')

    cursor = db.execute("SELECT COUNT(*) From users WHERE username = ?;", username)
    count = cursor.fetchone()[0]
    print(count)
    
    if count > 0:
        return {
            "error": "Username Taken!"
        }, 401

    db.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (username, password, minecraft_uuid, discord_id) )

    return {
        "success": "Account Created!"
    }, 200

@app.route('/chat/')
def chat():
    return open(os.path.join(ROOT, 'resources', 'chat', 'chat.html')).read()

@app.route('/createAccount/')
def account():
    return open(os.path.join(ROOT, 'resources', 'account_creation', 'account.html')).read()


@app.route('/api/messageIn/', methods=['POST'])
def api():
    data = request.get_json()
    print(data)

    if(check_is_command(data.get("platform"), data.get("msg"), data.get("name"))):
        return {
            "status": "command"
        }, 200

    broadcast_message(data.get("platform"), data.get("name"), data.get("msg"))

    return {
        "status": "sent"
    }, 200

@app.route('/api/webMessageIn/', methods=['POST'])
def web_api():
    data = request.get_json()
    user = verify_user(data.get("token"))
    print(user)

    if user is None:
        return {
            "error": "invalid_token"
        }, 401

    if(check_is_command("Web", data.get("msg"), user.get("name"))):
        return {
            "status": "command"
        }, 200

    broadcast_message("Web", user.get("name"), data.get("msg"))

    return {
        "status": "sent"
    }, 200


@app.route('/resources/<path:text>', methods=['GET', 'POST'])
def resource(text):
    file_path = os.path.join(ROOT, 'resources', text)

    if not os.path.isfile(file_path):
        return "File not found", 404

    # For non-image files, just send the file directly
    return send_file(file_path)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print(f'Received: {data}')
    emit('message_response', {'message': 'Message received'})

def check_is_command(platform, message, username):
    if message.startswith("!commands"):
        broadcast_message_to_platform(platform, "Available Commands:\n\t!commands\n\t!hereOnly\n\t!time")
        return True
    if message.startswith("!hereOnly"):
        broadcast_message_to_platform(platform, "Local Msg From "+username+": " + message.split("!hereOnly")[1])
        return True
    if message.startswith("!time"):
        from datetime import datetime
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        broadcast_message_to_platform(platform, "Current Server Time: " + date_str)
        return True
    return False


def broadcast_message(platform, username, message):
    print(platform, username, message)
    data = {
        "platform": platform,
        "name": username,
        "msg": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    if platform != "DC":
        url = "http://127.0.0.1:5000/api/messageIn/"
        response = requests.post(url, json=data, headers=headers, timeout=10)
    if platform != "MC":
        url = "http://quilt.duckdns.org:8080/api/messageIn/"
        response = requests.post(url, json=data, headers=headers, timeout=10)

        #print("Status Code:", response.status_code)
        #print("Response Body:", response.text)

    socketio.emit('broadcast_message', {'platform': platform, 'username': username, 'message': message})

def broadcast_message_to_platform(platform, message):
    print("Command Detected! Sending to " + platform)
    data = {
        "platform": "SYS",
        "name": "Com",
        "msg": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    if platform == "DC":
        url = "http://127.0.0.1:5000/api/messageIn/"
        response = requests.post(url, json=data, headers=headers, timeout=10)
    if platform == "MC":
        url = "http://quilt.duckdns.org:8080/api/messageIn/"
        response = requests.post(url, json=data, headers=headers, timeout=10)

        #print("Status Code:", response.status_code)
        #print("Response Body:", response.text)

    if platform == "Web":
        socketio.emit('broadcast_message', {'platform': "SYS", 'username': "Com", 'message': message})
    
def verify_user(token):
    try:
        user_code = fernet.decrypt(token.encode()).decode()
        username, password, _ = user_code.split("_")
        return user_exists_in_sql(username, password)
    except:
        return False


def user_exists_in_sql(username, password):
    cursor = db.execute("SELECT * FROM users WHERE username = ?;", username)
    result = cursor.fetchone()
    if result is None:
        return None
    return {
        "name": result[0],
        "password": result[1]
    }

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=80)