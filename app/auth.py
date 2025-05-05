import face_recognition
import numpy as np
from sqlalchemy.orm import Session
from app.models import User

def authenticate_user_from_np_image(np_image, db: Session):
    unknown_encodings = face_recognition.face_encodings(np_image)
    if not unknown_encodings:
        return None

    unknown_encoding = unknown_encodings[0]
    users = db.query(User).all()

    for user in users:
        known_encoding = np.frombuffer(user.encoding, dtype=np.float64)
        match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
        if match:
            return user.username
    return None
