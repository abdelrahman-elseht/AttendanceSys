import face_recognition
import os
import numpy as np
from pathlib import Path

KNOWN_DIR = "known_faces"


KNOWN_DIR = os.path.join(os.path.dirname(__file__), "known_faces")
TEST_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "test_faces", "2.jpg")
known_encodings = []
known_names = []

print(f"[INFO] Loading known faces from '{KNOWN_DIR}'...")

for filename in os.listdir(KNOWN_DIR):
    if filename.lower().endswith((".jpg", ".png")):
        image_path = os.path.join(KNOWN_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])
            print(f"Loaded: {filename}")
        else:
            print(f"No face found in {filename}")

print(f"Total known faces loaded: {len(known_names)}")

print(f"[INFO] Testing recognition on '{TEST_IMAGE_PATH}'...")
test_image = face_recognition.load_image_file(TEST_IMAGE_PATH)
test_encodings = face_recognition.face_encodings(test_image)

if not test_encodings:
    print("No face found in test image.")
    exit()

test_encoding = test_encodings[0]
results = face_recognition.compare_faces(known_encodings, test_encoding)
distances = face_recognition.face_distance(known_encodings, test_encoding)

if True in results:
    best_match_index = np.argmin(distances)
    recognized_name = known_names[best_match_index]
    print(f"Match found: {recognized_name} (Distance: {distances[best_match_index]:.4f})")
else:
    print("No match found. Face is unknown.")
