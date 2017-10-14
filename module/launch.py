from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    name = 'Alex'
    path = '/static/PandaLaotie1.png'
    return render_template('Test.html',var1 = name, var2 = path)

if __name__ == '__main__':
    app.run()
