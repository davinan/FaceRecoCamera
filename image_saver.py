import cv2
import voice2text
import threading

def write_image(image, v2t):
    name = v2t.v2t()
    cv2.imwrite(name + ".jpg", image)

if __name__ == "__main__":
    img= cv2.imread("alex.jpg")
    v2t = voice2text.voice2text()
    t = threading.Thread(target=write_image, args=(img, v2t))
    t.start()