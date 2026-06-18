import os
import cv2
from hsemotion_onnx.facial_emotions import HSEmotionRecognizer

EMOTION_LABELS = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]

#Analizes a photo and returns a vector of emotions using the HSEmotion model.
#Takes a string representing a file path or a numpy array representing an image (BGR or RGB).
#Returns a dict with emotion labels as keys (anger, contempt, disgust, fear, happiness, neutral, sadness, surprise)
#and float softmax probabilities as values.
#Throws FileNotFoundError if the file path is wrong.
def hsemotion_to_vector(image):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
        frame = cv2.imread(image)
    else:
        frame = image if image.shape[-1] == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    recognizer = HSEmotionRecognizer(model_name="enet_b0_8_best_afew")
    _, scores = recognizer.predict_emotions(frame, logits=False)
    return {label: float(prob) for label, prob in zip(EMOTION_LABELS, scores)}
