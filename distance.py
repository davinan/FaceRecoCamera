import face_recognition
def calc(known_face_encodings, face_encoding_to_check):
    return list(face_recognition.face_distance(known_face_encodings, face_encoding_to_check))