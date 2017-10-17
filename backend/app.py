from flask import Flask, jsonify, make_response, request
import json
from datetime import timedelta
from functools import update_wrapper, wraps
from flask_sqlalchemy import SQLAlchemy
import random, string
import bcrypt

config = {}

with open("config.json") as json_data:
	config = json.loads(json_data.read())
	json_data.close()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['sql_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    token = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.username

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    sender_id = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

    def __repr__(self):
        return '<Message %r>' % self.id

@app.before_first_request
def before_first_req():
    db.create_all()

INVALID_METHOD_RESPONSE = {
    "code": 405,
    "message": "Method Not Allowed"
}

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(INVALID_METHOD_RESPONSE)

@app.route("/api/messages", methods=["GET"])
def getAllMessages():
    result = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    data = {"code": 200}
    resultt = []
    for f in result:
        f2 = {}
        f2['id'] = f.id
        f2['content'] = f.content
        f2['sender_id'] = f.sender_id
        f2['timestamp'] = f.timestamp
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

    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # TODO If possible, make this one query instead of two
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return jsonify(USER_ALREADY_EXISTS_RESPONSE)
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify(USER_ALREADY_EXISTS_RESPONSE)

    user = User()
    token = generate_token()
    user.username = username
    user.password = password
    user.email = email
    user.token = token
    db.session.add(user)
    db.session.commit()
    result = {}
    result['id'] = user.id
    result['username'] = user.username
    result['token'] = user.token
    result['email'] = user.email
    return jsonify(result)

@app.route("/api/login", methods=["POST"])
def login():
    f = request.get_json()
    if not f:
        return jsonify({"code": 400, "message": "Bad Request"})
    username = f.get("username")
    password = f.get("password")
    user = User.query.filter_by(email=username).first()
    if not user:
        user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(INVALID_CREDENTIALS)
    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify(INVALID_CREDENTIALS)
    result = {}
    result['id'] = user.id
    result['username'] = user.username
    result['token'] = user.token
    result['email'] = user.email
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
