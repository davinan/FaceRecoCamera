from flask import Flask, render_template

import db_wrapper
import os



app = Flask(__name__)

@app.route("/")
def hello():

    DIRECTORY = "../yilun/static/Portrait/"
    nameList = []
    pathList = []
    for f in os.listdir(DIRECTORY):
        if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
            nameList.append(f.split(".")[0])
            pathList.append('/static/'+ f.split(".")[0] + '.jpg')
    return render_template('test.html',var1 = nameList, var2 = pathList)

@app.route('/Video')
def index():
    return render_template('Video.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run()
