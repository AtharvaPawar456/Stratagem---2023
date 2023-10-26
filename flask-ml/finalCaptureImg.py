from flask import Flask, render_template, Response, request,redirect, jsonify
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import pyrebase
import time
import random
import json

config = {
  "apiKey": "AIzaSyDgz34RIMvnV95tfI0QVL0yLF_3IlN8nvU",
  "authDomain": "firewebtest-acd85.firebaseapp.com",
  "databaseURL": "https://firewebtest-acd85-default-rtdb.firebaseio.com",
  "projectId": "firewebtest-acd85",
  "storageBucket": "firewebtest-acd85.appspot.com",
  "messagingSenderId": "355676175409",
  "appId": "1:355676175409:web:9d207ac8d11828c1382910",
  "measurementId": "G-6Z60DDCB8Y"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()


global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
# net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


# def detect_face(frame):
#     global net
#     (h, w) = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
#         (300, 300), (104.0, 177.0, 123.0))   
#     net.setInput(blob)
#     detections = net.forward()
#     confidence = detections[0, 0, 0, 2]

#     if confidence < 0.5:            
#             return frame           

#     box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
#     (startX, startY, endX, endY) = box.astype("int")
#     try:
#         frame=frame[startY:endY, startX:endX]
#         (h, w) = frame.shape[:2]
#         r = 480 / float(h)
#         dim = ( int(w * r), 480)
#         frame=cv2.resize(frame,dim)
#     except Exception as e:
#         pass
#     return frame

isMatch = "400"
getToken = "34535"
takeImg = True
apiresponse = {
        'status': isMatch,
        'token': getToken
                        }



def readRdb(val):
    global isMatch, getToken
    users = db.child("patients").child("userid").child(val).get()
    resId = users.val()["id"]
    resStatus = users.val()["userStatus"]
    restoken = users.val()["token"]
    getToken = restoken
    isMatch = resStatus

    # print("id",resId)
    # print("userStatus", resStatus)

def GenRandomToken(val):
    def randN(N):
        min = pow(10, N-1)
        max = pow(10, N) - 1
        return random.randint(min, max)
    tokenres = randN(5)
    print(tokenres)
    db.child("patients").child("userid").child(val).child("token").set(tokenres)

    # return tokenres


def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame, takeImg, apiresponse, isMatch
    while True:
        success, frame = camera.read() 
        if success:
            # if(face):                
            #     frame= detect_face(frame)
            # if(grey):
            #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # if(neg):
            #     frame=cv2.bitwise_not(frame)    
            if(capture):
                capture=0
                # now = datetime.datetime.now()
                # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                p = os.path.sep.join(['shots', "1.jpg"])
                cv2.imwrite(p, frame)

                time.sleep(0.2)
                # upload temp image to firebase
                imgFile1 = "shots/1.jpg"
                filenamefb = "1.jpg"
                check_fileimgFile1 = os.path.isfile(imgFile1)# print(check_file)
                if check_fileimgFile1:
                    # print("file uploaded on firebase")
                    storage.child("temp").child(filenamefb).put(imgFile1)

                time.sleep(0.2)
                readRdb("1")
                GenRandomToken("1")

                takeImg = False
                # return jsonify(apiresponse)
                # if isMatch== "200":
                return redirect('/')
                # return redirect('TokenShow.html', params=params)


            if (takeImg):
                if(rec):
                    rec_frame=frame
                    frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                    frame=cv2.flip(frame,1)
                
                    
                try:
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass
                
                
        else:
            pass


@app.route('/')
def index():     
    print(isMatch)           
    if isMatch== "200":
        return redirect('/token')
    return render_template('myverify.html')

@app.route('/token')
def tokenpage():
    params = jsonify(apiresponse)
    return render_template('TokenShow.html', data=apiresponse["token"])


    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        # elif  request.form.get('grey') == 'Grey':
        #     global grey
        #     grey=not grey
        # elif  request.form.get('neg') == 'Negative':
        #     global neg
        #     neg=not neg
        # elif  request.form.get('face') == 'Face Only':
        #     global face
        #     face=not face 
        #     if(face):
        #         time.sleep(4)   
        # elif  request.form.get('stop') == 'Stop/Start':
            
        #     if(switch==1):
        #         switch=0
        #         camera.release()
        #         cv2.destroyAllWindows()
                
        #     else:
        #         camera = cv2.VideoCapture(0)
        #         switch=1
        # elif  request.form.get('rec') == 'Start/Stop Recording':
        #     global rec, out
        #     rec= not rec
        #     if(rec):
        #         now=datetime.datetime.now() 
        #         fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #         out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
        #         #Start new thread for recording the video
        #         thread = Thread(target = record, args=[out,])
        #         thread.start()
        #     elif(rec==False):
        #         out.release()
                          
                 
    elif request.method=='GET':
        return render_template('myverify.html')
    # return render_template('myverify.html')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8080)
    
camera.release()
cv2.destroyAllWindows()     