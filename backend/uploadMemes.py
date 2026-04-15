import os
from pymongo import MongoClient
from bson.binary import Binary

# Connect to DB
client = MongoClient("mongodb+srv://GroupAdmin:7Sja9gih3Z78g3Z1@memematch.taqbveo.mongodb.net/?retryWrites=true&w=majority")
db = client["meme_match_db"]
collection = db["safeMemes"]

# Folder containing your images
IMAGE_FOLDER = "C:/Users/kelle/OneDrive/Desktop/WebsiteProject/MemeticLink/backend/safeMemes"  
def upload_images(folder_path):
    # Get all image files
    valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    
    print(f"Found {len(files)} images to upload", flush=True)

    for i, filename in enumerate(files):
        filepath = os.path.join(folder_path, filename)
        
        # Skip if already uploaded
        existing = collection.find_one({"filename": filename})
        if existing:
            print(f"  Skipping {filename} — already in DB", flush=True)
            continue

        try:
            with open(filepath, "rb") as f:
                image_data = Binary(f.read())

            collection.insert_one({
                "filename": filename,
                "data": image_data,
                "content_type": "image/jpeg"
            })

            print(f"  [{i+1}/{len(files)}] Uploaded {filename}", flush=True)

        except Exception as e:
            print(f"  [{i+1}/{len(files)}] Failed {filename} — {e}", flush=True)
            continue

    print("Done!")

if __name__ == "__main__":
    upload_images(IMAGE_FOLDER)