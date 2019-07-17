from flask import Flask, escape, request, jsonify

app = Flask(__name__)

@app.route('/count')
def count():
    return jsonify({"hello": "world"})