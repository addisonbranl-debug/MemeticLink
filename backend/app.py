import random 

from flask import Flask, jsonify, Response, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.binary import Binary
import numpy as np
import cv2
from photoModels.photoToVector import photo_to_vector
from photoModels.orbToVector import orb_to_vector
from photoModels.mediapipeToVector import mediapipe_to_vector
from photoModels.hsemotionToVector import hsemotion_to_vector
from photoModels.hogToVector import hog_to_vector
from photoModels.facenetToVector import facenet_to_vector
from photoModels.clipToVector import clip_to_vector
from euclidianVectorComparison import euclidean_distance

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://GroupAdmin:7Sja9gih3Z78g3Z1@memematch.taqbveo.mongodb.net/?retryWrites=true&w=majority")
db = client["meme_match_db"]
imgCollection = db["fs.chunks"]
embCollection = db["RealEncodings"]
memeCollection = db["memes"]
numMemes = embCollection.count_documents({})
VECTORLENGTH = 8100

def safeToList(vector):
    if isinstance(vector, np.ndarray):
        return vector.tolist()
    elif isinstance(vector, dict):
        return list(vector.values())
    elif isinstance(vector, list):
        return vector
    else:
        raise ValueError(f"Unexpected vector type: {type(vector)}")

def normalizeVector(vector):   
    vec = np.array(vector, dtype=np.float64)
    print(f"vec size: {len(vec)}", flush=True)
    if len(vec) == 0:
        print("empty vec size detected", flush=True)
        vec = np.zeros(512)
        print(f"padded vec size: {len(vec)}", flush=True)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

def total_distance(enc_a,enc_b):
    sum = 0.0
    keys = ["otv_encoding", "hsv_encoding", "hov_encoding", "ftv_encoding", "ctv_encoding"]
    # keys = ["hov_encoding"]

    for key in keys:
        print(f"normalizing : {key}",flush=True)
        a = normalizeVector(enc_a[key])
        b = normalizeVector(enc_b[key])
        sum += np.linalg.norm(a - b)
    
    return sum

@app.route("/api/upload", methods=["POST"])
def matchMeme():
    embeddings = embCollection.find({})
    if "image" not in request.files:
            return {"error": "No image provided"}, 400
    
    file = request.files["image"]
    
    imageBytes = np.frombuffer(file.read(), np.uint8)
    imageNP = cv2.imdecode(imageBytes, cv2.IMREAD_COLOR)

    try: 
        #generate vectors for user capture
        oTVector = orb_to_vector(imageNP)
        hSVector = hsemotion_to_vector(imageNP)
        hOVector = hog_to_vector(imageNP)
        cTVector = clip_to_vector(imageNP)
        fTVector = facenet_to_vector(imageNP)

        #convert vectors to python lists and store in user ENC to replicate db format

        userEnc = {
            "otv_encoding" : safeToList(oTVector),
            "hsv_encoding": safeToList(hSVector),
            "hov_encoding": safeToList(hOVector),
            "ftv_encoding": safeToList(fTVector),
            "ctv_encoding": safeToList(cTVector),
        }

    except ValueError as e:
        return {"error": str(e)}, 400
    except FileNotFoundError as e:
        return {"error": str(e)}, 400

    minDistance = float("inf")
    matchID = ""
    for entry in embeddings:
        dist = total_distance(entry,userEnc)
        if dist < minDistance:
            matchID = entry["fs_chunk_id"]
            minDistance = dist
    
    print(f"matching photo id = {matchID}", flush = True)
    doc = imgCollection.find_one({"_id" : matchID})   
    if doc is None:
        print("none doc", flush=True)
        return {"error": f"No document found with filename"}, 404
    
    if "data" not in doc:
        print("no data in doc",flush=True)
        return {"error": "Document found but has no 'data' field"}, 404
    
    print(f"files_id of match = {doc['files_id']}",flush=True)

    return Response(bytes(doc["data"]), mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True, port=5000)


