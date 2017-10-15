from flask import Flask, render_template

from db_wrapper import db_wrapper
import os



app = Flask(__name__)
conn = db_wrapper()

@app.route("/")
def hello():

    DIRECTORY = "../yilun/static/Portrait/"
    nameList = []
    visitList = []
    pathList = []
    for f in os.listdir(DIRECTORY):
        if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
            nameList.append(f.split(".")[0])
            # countList.append(conn.name_count(f.split(".")[0]))
            visitList.append(f.split(".")[0])
            pathList.append('/static/'+ f.split(".")[0] + '.jpg')


    totalNum = conn.total_count()
    ageAve = conn.age_average()
    genRto = conn.gender_ratio()
    glsRto = conn.glass_ratio()
    maxVisit = conn.max_visit()
    # print(nameList)
    print(totalNum)
    return render_template('test.html',var1 = nameList, visit_List = visitList, var2 = pathList, total_count = totalNum, age_Ave = ageAve, gen_Rto = genRto, gls_Rto = glsRto, max_visit = maxVisit)

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
