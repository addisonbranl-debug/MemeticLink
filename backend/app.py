from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

test = [
    {"id": 1, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme1.jpg"},
    {"id": 2, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme2.jpg"},
    {"id": 3, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme3.jpg"},
    {"id": 4, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme4.jpg"},
    {"id": 5, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme5.jpg"},
    {"id": 6, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme6.jpg"},
    {"id": 7, "filepath": "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/imgs/meme7.jpg"}
    ]


@app.route("/api/memetic", methods=["GET"])
def get_test():
    return jsonify(test)

@app.route("/api/image/<int:image_id>", methods=["GET"])
def get_image(image_id):
    return send_file(test[image_id-1]["filepath"], mimetype="image/jpg")

if __name__ == "__main__":
    app.run(debug=True, port=5000)