import os
import face_recognition
import cv2
import mc_face
def img_parser():
    name_list = []
    encoding_list = []
    glass_list = []
    age_list = []
    gender_list = []
    DIRECTORY = "../HackGT/"
    for f in os.listdir(DIRECTORY):
        if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
            temp_img = face_recognition.load_image_file(f)
            temp_encoding = face_recognition.face_encodings(temp_img)
            if len(temp_encoding) > 0:
                temp_specs = mc_face.analyse(f)
                encoding_list.append(temp_encoding[0])
                name_list.append(f.split(".")[0])
                age_list.append(temp_specs[0])
                gender_list.append(temp_specs[1])
                glass_list.append(temp_specs[2])
    # print([name_list, encoding_list, age_list, gender_list, glass_list])
    return [name_list, encoding_list, age_list, gender_list, glass_list]
if __name__ == "__main__" :
    img_parser()