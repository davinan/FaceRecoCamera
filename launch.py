from flask import Flask, render_template
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
            pathList.append('/static/Portrait/'+ f.split(".")[0] + '.jpg')
    return render_template('Test.html',var1 = nameList, var2 = pathList)

if __name__ == '__main__':
    app.run()
