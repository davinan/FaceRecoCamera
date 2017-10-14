#coding:utf-8
import multiprocessing
import time
import server
import face_reco
import cv2
from flask import Flask, render_template, Response

# Build a pipe


# def read(pipe):
#     while True:
#         value = pipe.recv()
#         print 'Get %s from queue.' % value
 
# p =multiprocessing.Pipe()
# # Pass an end of the pipe to process 1
# p1   = multiprocessing.Process(target=face_reco.reco, args=(p[0],))
# # Pass the other end of the pipe to process 2
# # p2   = multiprocessing.Process(target=read, args=(p[1],))
# p1.start()
# # p2.start()
# p1.join()

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# def gen():
#     while True:
#         frame = p.recv()
#         cv2.imshow("TEST",frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# app.run(host='0.0.0.0', debug=True)


# # p1.terminate()
# # p2.join()