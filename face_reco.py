import face_recognition
import cv2
import kinect
import img_file_parser
import voice2text
import threading

# Get a reference to webcam #0 (the default one)
class reco():
    def __init__(self):
        # threading.Thread.__init__(self)
        self.video_capture = cv2.VideoCapture(0)
        ret, self.frame = self.video_capture.read()

    def face_reco(self):
        temp = img_file_parser.img_parser()
        name_list = temp[0]
        # print(name_list)
        face_encoding_list = temp[1]
        age_list = temp[2]
        gender_list = temp[3]
        glass_list = temp[4]
        # Initialize some variables

        process_this_frame = True
        detected = False
        face_locations = []
        face_encodings = []
        face_names = []

        while True:

            # Grab a single frame of video
            ret, self.frame = self.video_capture.read()   # Local camera
            # frame = kinect.get_video()          # Kinect Camera
            self.frame = cv2.resize(self.frame, (640, 480))

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

            # Only process every other frame of video to save time
            if process_this_frame:
                face_locations = []
                face_encodings = []
                face_names = []
                face_ages = []
                face_gender = []
                face_glasses = []
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces(face_encoding_list, face_encoding, tolerance=0.6)
                    name = "Unknown"
                    age = "unknown"
                    gender = "unknown"
                    glass = "unknown"
                    try:
                        matchingFace = match.index(True)
                    except ValueError:
                        matchingFace = -1
                    faceLength = len(match)
                    
                    
                    if matchingFace == -1:
                        if detected:
                            largeNewName = raw_input("Input your name: ")
                            detected = False
                            if not largeNewName == "X" and not largeNewName == "x":
                                name_list.append(largeNewName)
                                face_encoding_list.append(face_encoding)
                                cv2.imwrite(largeNewName + ".jpg", small_frame)
                        else:
                            detected = True
                    else:
                        name = name_list[matchingFace]
                        if(len(age_list) > 0):
                            age = age_list[matchingFace]
                            gender = gender_list[matchingFace]
                            glass = glass_list[matchingFace]
                        detected = False
                        

                    face_names.append(name)
                    face_ages.append(age)
                    face_gender.append(gender)
                    face_glasses.append(glass)

            process_this_frame = not process_this_frame

            k = 0
            # Display the results
            for (top, right, bottom, left), name1 in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                age1 = face_ages[k]
                gender1 = face_gender[k]
                glass1 = face_glasses[k]
                k = k + 1
                # Draw a box around the face
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # # Draw a label with a name below the face
                cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom + 40), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.frame, name1, (left + 6, bottom - 6), font, 1, (0, 255, 0), 1)
                cv2.putText(self.frame, str(age1), (left + 6, bottom + 16), font, 0.4, (0, 255, 0), 1)
                cv2.putText(self.frame, gender1, (left + 6, bottom + 27), font, 0.4, (0, 255, 0), 1)
                cv2.putText(self.frame, glass1, (left + 6, bottom + 38), font, 0.4, (0, 255, 0), 1)

            # Display the resulting image
            cv2.imshow('Video', self.frame)
            cv2.imwrite("static/stream.jpg", self.frame)
            # pipe.send(self.frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release handle to the webcam
r = reco()
# r.start()
r.face_reco()
# video_capture.release()
# cv2.destroyAllWindows()