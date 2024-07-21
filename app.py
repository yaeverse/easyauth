# Yaeverse EastAuth - A simple authentication server.
# The software licensed under Mozilla Public License Version 2.0
# (c) 2024 Star Inc.

from flask import Flask, request, Response, jsonify
from flask_cors import CORS

import time

app = Flask(__name__)

CORS(app, supports_credentials=True)

users = {
    "admin": "admin",
    "user": "user"
}

tokens = {}


@app.route('/')
def about():
    return """
    <b>Yaeverse EastAuth</b>
    <hr />
    <p>A simple authentication server.</p>
    <p>(c) 2024 Star Inc.</p>
    """


@app.route('/api/authorize', methods=['POST'])
def authorize():
    if request.is_json:
        data = request.get_json()
        if not ("username" in data or "password" in data):
            return jsonify({
                "status": 400,
                "reason": "Bad Request"
            })
        if data["username"] in users:
            if data["password"] == users[data["username"]]:
                token = str(hash(time.time()))
                tokens[token] = data["username"]
                response = jsonify({
                    "status": 200,
                    "reason": token
                })
                if data.get("cookie"):
                    response.set_cookie(
                        key="kaguya_token",
                        value=token,
                        path="/"
                    )
                return response
        return jsonify({
            "status": 401,
            "reason": "Unauthorized"
        })
    else:
        return Response(
            "Bad Request",
            status=400,
        )


@app.route('/api/verify', methods=['GET'])
def web_client_verify():
    identification = request.cookies.get("kaguya_token")
    if identification in tokens:
        return jsonify({
            "status": 200,
            "reason": tokens[identification]
        })
    return jsonify({
        "status": 401,
        "reason": "Unauthorized"
    })


@app.route('/api/verify', methods=['POST'])
def verify():
    if request.form:
        if "authToken" not in request.form:
            return jsonify({
                "status": 400,
                "reason": "Bad Request"
            })
        if request.form["authToken"] in tokens:
            return jsonify({
                "status": 200,
                "reason": tokens[request.form["authToken"]]
            })
        return jsonify({
            "status": 401,
            "reason": "Unauthorized"
        })
    else:
        return Response(
            "Bad Request",
            status=400,
        )
