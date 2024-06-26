# -*- coding: utf-8 -*-
# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : main.py                 #
# ----------------------------------------------- #

import json
import time

from flask import Flask, request

import config
from handler import *

app = Flask(__name__)


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        if request.method == "POST":
            result = request.data.decode("utf-8")
            print(request.data)
            print(type(result))
            if result.find("telegram") != -1:
                data = request.get_json()
            else:
                data = {
                    "key": "xiabing-bot",
                    "telegram": -1001442727075,
                    "msg": result
                }
            key = data["key"]

            if key == config.sec_key:
                print(get_timestamp(), "Alert Received & Sent!")
                send_alert(data)
                return "Sent alert", 200

            else:
                print("[X]", get_timestamp(), "Alert Received & Refused! (Wrong Key)")
                return "Refused alert", 400

    except Exception as e:
        print("[X]", get_timestamp(), "Error:\n>", e)
        return "Error", 400


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8081)
