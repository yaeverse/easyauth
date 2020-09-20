"""
    KIaguya - The opensource instant messaging framework.
    ---
    Copyright 2020 Star Inc.(https://starinc.xyz)

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from flask import Flask, request, Response, render_template, jsonify, make_response

import time

app = Flask(__name__)

users = {
    "admin": "admin",
    "user": "user"
}

tokens = {}


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/about')
def about():
    return """
    Kaguya - Authorization
    ===
    The API Server is used for authorize and verify the identity for Kaguya.

    (c)2020 Star Inc.
    """


@app.route('/success')
def success():
    return "Success"


@app.route('/authorize', methods=['POST'])
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
                response = make_response(jsonify({
                    "status": 200,
                    "reason": "Success"
                }))
                token = str(hash(time.time()))
                tokens[token] = data["username"]
                response.set_cookie("kaguya_token", token)
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


@app.route('/verify', methods=['POST'])
def issueToken():
    if request.is_json:
        data = request.get_json()
        if "authToken" not in data:
            return jsonify({
                "status": 400,
                "reason": "Bad Request"
            })
        if data["authToken"] in tokens:
            return jsonify({
                "status": 200,
                "reason": tokens[data["authToken"]]
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
