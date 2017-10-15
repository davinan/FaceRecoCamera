import face_recognition
import cv2
import kinect
import img_file_parser
import voice2text
import threading
import mc_face
import os
import tts
import db_wrapper

# Get a reference to webcam #0 (the default one)
class face_reco():
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.db = db_wrapper.db_wrapper()

    def reco(self):
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
            ret, frame = self.video_capture.read()   # Local camera
            # frame = kinect.get_video()          # Kinect Camera
            frame = cv2.resize(frame, (640, 480))

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

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
                    match = face_recognition.compare_faces(face_encoding_list, face_encoding, tolerance=0.5)
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
                            # print("New face found, please say your name for the record\n")
                            tts.tts("New face found, please say your name for the record")
                            # largeNewName = raw_input("Input your name: ")

                            # largeNewName = voice2text()
                            # t = voice2text()
                            # x = threading.Thread(target=t.v2t)
                            # x.start()
                            
                            t = voice2text.voice2text()
                            try:
                                largeNewName = t.v2t()
                            except:
                                tts.tts("Timeout")
                                largeNewName = "x"

                            detected = False
                            if not largeNewName == "X" and not largeNewName == "x":
                                name_list.append(largeNewName)
                                face_encoding_list.append(face_encoding)

                                indi = face_encodings.index(face_encoding)
                                (top, right, bottom, left) = face_locations[indi]
                                roi = frame[int(top * 4 * 0.7): min(int(bottom * 4 * 1.4) , 480), int(left *4 * 0.7):min(int(right*4*1.4), 640)]
                                # print(type(roi))

                                ct = self.db.name_count(largeNewName)
                                cv2.imwrite(largeNewName + str(ct + 1) + ".jpg", roi)
                                os.system("cp \"" + largeNewName + str(ct + 1) + ".jpg\"" + "  ../HackGT/yilun/static/Portrait/")
                                temp_specs = mc_face.analyse(largeNewName +str(ct + 1)+ ".jpg")

                                if not len(temp_specs) == 0:
                                    age_list.append(temp_specs[0])
                                    gender_list.append(temp_specs[1])
                                    glass_list.append(temp_specs[2])
                                    try:
                                        self.db.add_person_full(largeNewName, largeNewName + str(ct + 1), temp_specs[0],
                                                       temp_specs[1] == "Male", temp_specs[2] == "ReaderGlasses")
                                    except:
                                        pass
                                else:
                                    age_list.append(99)
                                    gender_list.append("UNKNOWN")
                                    glass_list.append("UNKNOWN")
                                    try:
                                        self.db.add_person(largeNewName, largeNewName + str(ct + 1))
                                    except:
                                        pass

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
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom + 40), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX

                cv2.putText(frame, name1, (left + 6, bottom - 6), font, 1, (0, 255, 0), 1)
                cv2.putText(frame, str(age1), (left + 6, bottom + 16), font, 0.4, (0, 255, 0), 1)
                cv2.putText(frame, gender1, (left + 6, bottom + 27), font, 0.4, (0, 255, 0), 1)
                cv2.putText(frame, glass1, (left + 6, bottom + 38), font, 0.4, (0, 255, 0), 1)

            # Display the resulting image
            # cv2.putText(frame,"What's your name?",(320,240),cv2.FONT_HERSHEY_DUPLEX,1,(0, 255, 0), 1)
            cv2.imshow('Video', frame)
            cv2.imwrite("static/Stream.jpg", frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__" :
    r = face_reco()
    # # r.start()
    r.reco()
# Release handle to the webcam
# r = face_reco()
# # r.start()
# r.reco()
# video_capture.release()
# cv2.destroyAllWindows()

