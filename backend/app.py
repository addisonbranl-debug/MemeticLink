from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

test = [
    {"id": 1, "text": "hello this is a test"}
]

@app.route("/api/memetic", methods=["GET"])
def get_test():
    return jsonify(test)

if __name__ == "__main__":
    app.run(debug=True, port=5000)