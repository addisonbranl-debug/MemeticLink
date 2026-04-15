import numpy as np
from pymongo import MongoClient
from bson import ObjectId
import cv2
from photoModels.photoToVector import photo_to_vector
from photoModels.orbToVector import orb_to_vector
from photoModels.mediapipeToVector import mediapipe_to_vector
from photoModels.hsemotionToVector import hsemotion_to_vector
from photoModels.hogToVector import hog_to_vector
from photoModels.facenetToVector import facenet_to_vector
from photoModels.clipToVector import clip_to_vector


def safeToList(vector):
    if isinstance(vector, np.ndarray):
        return vector.tolist()
    elif isinstance(vector, dict):
        return list(vector.values())
    elif isinstance(vector, list):
        return vector
    else:
        raise ValueError(f"Unexpected vector type: {type(vector)}")

# Connect to DB
client = MongoClient("mongodb+srv://GroupAdmin:7Sja9gih3Z78g3Z1@memematch.taqbveo.mongodb.net/?retryWrites=true&w=majority")
db = client["meme_match_db"]
imgCollection = db["fs.chunks"]
embCollection = db["RealEncodings"]
memeCollection = db["memes"]

def encodeAllImages():
    docs = list(imgCollection.find({}))
    print(f"Found {len(docs)} images", flush=True)

    for i, doc in enumerate(docs):
        print(f"Processing {i+1}/{len(docs)}...", flush=True)

        # Skip if already encoded
        existing = embCollection.find_one({"fs_chunk_id": doc["_id"]})
        if existing:
            print(f"  Skipping {doc['_id']} — already encoded", flush=True)
            continue

        try:
            # Convert stored bytes → numpy array
            imageBytes = np.frombuffer(bytes(doc["data"]), np.uint8)
            imageNp = cv2.imdecode(imageBytes, cv2.IMREAD_COLOR)

            if imageNp is None:
                print(f"  Skipping {doc['_id']} — failed to decode image", flush=True)
                continue

            # Generate emotion vector
            # pTVector = photo_to_vector(imageNp)
            print("ptv done")
            oTVector = orb_to_vector(imageNp)
            print(f"otv done — type: {type(oTVector)}")
            # mTVector = mediapipe_to_vector(imageNp)
            print("mtv done")
            hSVector = hsemotion_to_vector(imageNp)
            print(f"hsv done — type: {type(hSVector)}")
            hOVector = hog_to_vector(imageNp)
            print(f"hov done — type: {type(hOVector)}")
            cTVector = clip_to_vector(imageNp)
            print(f"ctv done — type: {type(cTVector)}")
            fTVector = facenet_to_vector(imageNp)
            print(f"ftv done — type: {type(fTVector)}")
            

            # Store encoding linked to the original image
            embCollection.insert_one({
                "fs_chunk_id": doc["_id"],       # reference back to original image
                # "ptv_encoding": pTVector.tolist(),
                "otv_encoding": safeToList(oTVector),
                # "mtv_encoding": mTVector.tolist(),
                "hsv_encoding": safeToList(hSVector),
                "hov_encoding": safeToList(hOVector),
                "ftv_encoding": safeToList(fTVector),
                "ctv_encoding": safeToList(cTVector),
            })

            print(f"  Stored encoding for {doc['_id']}", flush=True)

        except ValueError:
            print(f" no face detected", flush=True)
            embCollection.insert_one({
                "fs_chunk_id": doc["_id"],       # reference back to original image
                # "ptv_encoding": pTVector.tolist(),
                "otv_encoding": safeToList(oTVector),
                # "mtv_encoding": mTVector.tolist(),
                "hsv_encoding": safeToList(hSVector),
                "hov_encoding": safeToList(hOVector),
                "ftv_encoding": [],
                "ctv_encoding": safeToList(cTVector),
            })
            print(f"  Stored encoding for {doc['_id']}", flush=True)
        except Exception as e:
            print(f"  Skipping {doc['_id']} — unexpected error: {e}", flush=True)

if __name__ == "__main__":
    encodeAllImages()
    print("Done!")