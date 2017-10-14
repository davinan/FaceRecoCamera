import os
import face_recognition
import cv2
def img_parser():
    name_list = []
    encoding_list = []
    DIRECTORY = "../HackGT"
    for f in os.listdir(DIRECTORY):
        if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
            temp_img = face_recognition.load_image_file(f)
            temp_encoding = face_recognition.face_encodings(temp_img)
            if len(temp_encoding) > 0:
                encoding_list.append(temp_encoding[0])
                name_list.append(f.split(".")[0])
                print(f.split(".")[0])
    return [name_list, encoding_list]
if __name__ == "__main__" :
    img_parser()