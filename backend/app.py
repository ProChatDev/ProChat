from flask import Flask, jsonify, make_response, request
import json
from datetime import timedelta
from functools import update_wrapper, wraps
import pymongo
import random, string
import bcrypt

config = {}

with open("config.json") as json_data:
	config = json.loads(json_data.read())
	json_data.close()

app = Flask(__name__)
db_client = pymongo.MongoClient(config.get("mongo_uri", "mongodb://localhost:27017/"))
db = db_client[config.get('mongo_database_name', "prochat")]
users = db.users
messages = db.messages

def generate_id():
    import time
    f = 1508320834
    f2 = int(round(time.time() * 1000))
    return ((f2 - f) << 10) + ((1<<10)-0)

INVALID_METHOD_RESPONSE = {
    "code": 405,
    "message": "Method Not Allowed"
}

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(INVALID_METHOD_RESPONSE)

@app.route("/api/messages", methods=["GET"])
def getAllMessages():
    result = messages.find({})
    data = {"code": 200}
    resultt = []
    for f in result:
        f2 = {}
        f2['id'] = f['id']
        f2['content'] = f["content"]
        sender = users.find({"_id":f['sender_id']})
        f2['sender_id'] = f['sender_id']
        senderr = {}
        senderr['username'] = sender['username']
        f2['timestamp'] = f['timestamp']
        resultt.append(f2)
    data['result'] = resultt
    return jsonify(data)

USER_ALREADY_EXISTS_RESPONSE = {
    "code": 409,
    "message": "A user with this email or username already exists"
}

INVALID_CREDENTIALS = {
    "code": 403,
    "message": "Invalid Credentials"
}

def generate_token():
    token = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(25))
    return token

@app.route("/api/register", methods=["POST"])
def register():
    f = request.get_json()
    if not f:
        return jsonify({"code": 400, "message": "Bad Request"})
    username = f.get("username")
    _password = f.get("password")
    email = f.get("email")

    if not username or not _password or not email:
        return jsonify({"code": 400, "message": "Bad Request"})

    password = bcrypt.hashpw(_password.encode('utf-8'), bcrypt.gensalt())

    # TODO If possible, make this one query instead of two
    user = users.find_one({"username":username})
    if user is not None:
        return jsonify(USER_ALREADY_EXISTS_RESPONSE)
    user = users.find_one({"email":email})
    if user is not None:
        return jsonify(USER_ALREADY_EXISTS_RESPONSE)

    user = {}
    token = generate_token()
    user['_id'] = generate_id()
    user['username'] = username
    user['password'] = password
    user['email'] = email
    user['token'] = token
    users.insert_one(user)
    result = {}
    result['id'] = user['_id']
    result['username'] = user['username']
    result['token'] = user['token']
    result['email'] = user['email']
    return jsonify(result)

@app.route("/api/login", methods=["POST"])
def login():
    f = request.get_json()
    if not f:
        return jsonify({"code": 400, "message": "Bad Request"})
    username = f.get("username")
    password = f.get("password")
    if not username or not password:
        return jsonify({"code": 400, "message": "Bad Request"})
    user = users.find_one({"email":username})
    if not user:
        user = users.find_one({"username":username})
    if not user:
        return jsonify(INVALID_CREDENTIALS)
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify(INVALID_CREDENTIALS)
    result = {}
    result['id'] = user['_id']
    result['username'] = user['username']
    result['token'] = user['token']
    result['email'] = user['email']
    return jsonify(result)

@app.errorhandler(404)
def notfound(e):
	data = {}
	data['code'] = 404
	data['message'] = "Page not found"
	return jsonify(data)

if __name__ == "__main__":
	# Not to be used for production
	app.run(port=config.get("port", 5000), debug=True)
