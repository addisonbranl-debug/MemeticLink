import cv2
import numpy as np
import os

IMAGE_FOLDER = "images"
SKIP_FRAMES = 5
HISTORY_SIZE = 5

# ── Build available analysis methods ─────────────────────────────────────────
# Each entry: (display_name, fn(image) -> np.ndarray)

analysis_methods = []

try:
    from photoToVector import photo_to_vector
    analysis_methods.append(("DeepFace", photo_to_vector))
except ImportError:
    pass

try:
    from hsemotionToVector import hsemotion_to_vector as _hse_raw
    def _hse_vec(img):
        d = _hse_raw(img)
        return np.array(list(d.values()), dtype=np.float32)
    analysis_methods.append(("HSEmotion", _hse_vec))
except ImportError:
    pass

try:
    from hogToVector import hog_to_vector
    analysis_methods.append(("HOG", hog_to_vector))
except ImportError:
    pass

try:
    from orbToVector import orb_to_vector
    analysis_methods.append(("ORB", orb_to_vector))
except ImportError:
    pass

try:
    from mediapipeToVector import mediapipe_to_vector
    analysis_methods.append(("MediaPipe", mediapipe_to_vector))
except ImportError:
    pass

try:
    from facenetToVector import facenet_to_vector
    analysis_methods.append(("FaceNet", facenet_to_vector))
except ImportError:
    pass

try:
    from clipToVector import clip_to_vector
    analysis_methods.append(("CLIP", clip_to_vector))
except ImportError:
    pass

if not analysis_methods:
    print("No analysis methods available. Install dependencies.")
    exit()

# ── Comparison methods ────────────────────────────────────────────────────────
from euclidianVectorComparison import euclidean_distance
from cosineVectorComparison import cosine_distance
from manhattanVectorComparison import manhattan_distance
from chebyshevVectorComparison import chebyshev_distance
from klDivergenceComparison import kl_divergence, jensen_shannon_divergence

comparison_methods = [
    ("Euclidean",       euclidean_distance),
    ("Cosine",          cosine_distance),
    ("Manhattan",       manhattan_distance),
    ("Chebyshev",       chebyshev_distance),
    ("KL Divergence",   kl_divergence),
    ("Jensen-Shannon",  jensen_shannon_divergence),
]

# ── State ─────────────────────────────────────────────────────────────────────
analysis_idx = 0
comparison_idx = 0
image_vectors = []  # list of {"filename": str, "vector": np.ndarray, "image": np.ndarray}


def precompute_vectors():
    global image_vectors
    name, fn = analysis_methods[analysis_idx]
    print(f"\nPrecomputing vectors using {name}...")
    image_vectors = []
    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(IMAGE_FOLDER, filename)
            try:
                vec = fn(path)
                img = cv2.imread(path)
                image_vectors.append({"filename": filename, "vector": vec, "image": img})
            except Exception as e:
                print(f"  Skipping {filename}: {e}")
    print(f"  Loaded {len(image_vectors)} vectors.")


precompute_vectors()

if not image_vectors:
    print("No images could be processed with the selected method.")
    exit()

# ── Webcam loop ───────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Keys: [A] cycle analysis method  [C] cycle comparison method  [Q] quit")

frame_count = 0
history = []
current_best_image = None
current_best_filename = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % SKIP_FRAMES == 0:
        _, analysis_fn = analysis_methods[analysis_idx]
        _, comparison_fn = comparison_methods[comparison_idx]
        try:
            vec = analysis_fn(frame)
            history.append(vec)
            if len(history) > HISTORY_SIZE:
                history.pop(0)
            smoothed = np.mean(history, axis=0)

            best_match = None
            min_dist = float("inf")
            best_image = None
            for ref in image_vectors:
                try:
                    dist = comparison_fn(smoothed, ref["vector"])
                except Exception:
                    dist = float("inf")
                if dist < min_dist:
                    min_dist = dist
                    best_match = ref["filename"]
                    best_image = ref["image"]

            if best_match != current_best_filename:
                current_best_filename = best_match
                current_best_image = best_image.copy() if best_image is not None else None
                print(f"Match: {current_best_filename}")
        except Exception:
            pass  # keep previous match on error

    analysis_name, _ = analysis_methods[analysis_idx]
    comparison_name, _ = comparison_methods[comparison_idx]
    cv2.putText(frame, f"Analysis: {analysis_name}  [A]",  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Compare:  {comparison_name}  [C]", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if current_best_filename:
        cv2.putText(frame, f"Match: {current_best_filename}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

    if current_best_image is not None:
        h = frame.shape[0]
        w = int(current_best_image.shape[1] * (h / current_best_image.shape[0]))
        ref_resized = cv2.resize(current_best_image, (w, h))
        combined = np.hstack((frame, ref_resized))
        cv2.imshow("MemeticLink", combined)
    else:
        cv2.imshow("MemeticLink", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("a"):
        analysis_idx = (analysis_idx + 1) % len(analysis_methods)
        history.clear()
        precompute_vectors()
    elif key == ord("c"):
        comparison_idx = (comparison_idx + 1) % len(comparison_methods)
        history.clear()

cap.release()
cv2.destroyAllWindows()
