from flask import Flask, request, make_response, jsonify
from datetime import datetime
from database import collection
from bson import json_util
import ujson

app = Flask(__name__)
last_data = {}


@app.post('/temperature')
def save_temperature():
    data = request.get_json()
    if data:
        try:
            last_data.update({
                "state": {
                    "value": data['state'].get('value', 0),
                    "status": data['state']['context'].get('status', "-")
                },
                "temperature": {
                    "value": data['temperature'].get('value', 0),
                    "status": data['temperature']['context'].get('status', "-")
                },
                "humidity": {
                    "value": data['humidity'].get('value', 0),
                    "status": data['humidity']['context'].get('status', "-")
                },
                "timestamp": datetime.utcnow()
            })

            collection.insert_one(last_data.copy())
            return jsonify({
                "success": True,
                "message": "Data terkirim!",
                "data": None
            })
        except IndexError:
            return jsonify({
                "success": False,
                "message": "Data invalid!",
                "data": None
            })
    else:
        return jsonify({
            "success": False,
            "message": "Data kosong!",
            "data": None
        })


@app.get("/temperature")
def get_temperature():
    if last_data:
        return jsonify({
            "success": True,
            "message": "Respon sukses!",
            "data": last_data
        })
    else:
        return jsonify({
            "success": False,
            "message": "Data kosong!",
            "data": None
        })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
