import face_recognition
import cv2
import main
import newFace

obama_image = face_recognition.load_image_file("fanzhe1.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

alex_image = face_recognition.load_image_file("alex1.jpg")
frame = cv2.resize(alex_image, (640, 480))

small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

# if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
face_locations = face_recognition.face_locations(small_frame)
face_encodings = face_recognition.face_encodings(small_frame, face_locations)

face_names = []
for face_encoding in face_encodings:
    print("Reached")
    # See if the face is a match for the known face(s)
    match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
    name = "Unknown"

    if match[0]:
        name = "fanzhe"
        print(name)
    else:
        newFace.storeNewFace("Alex",small_frame)
        print("New Name")

    face_names.append(name)

    # process_this_frame = not process_this_frame