from flask import Flask, render_template, Response, request, jsonify
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import pyrebase
import face_recognition

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
my_img = "ritikimg.jpg"
img2 = "app-ring.pngf2338300-9a87-4b62-a793-3781a95781bf"


# dbImg = "data/pawar.jpeg"
# Download Image
# storage.child("images").child(img2).download(filename='myS2.jpg',path=os.path.basename(img2))
# storage.child("images").child(img2).download(filename='myS2.jpg',path="data/")

userid1 = "0"
matchName = ""



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

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            if(capture):
                capture=0
                now = datetime.datetime.now()
                # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                p = os.path.sep.join(['shots', "verify1.jpg"])
                cv2.imwrite(p, frame)            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

def recog(userid):
    global matchName
    imgFile1 = "down1.jpg"
    imgFile2 = "down2.jpg"
    dbimg1 = "verify1.jpg"


    check_fileimgFile1 = os.path.isfile(imgFile1)# print(check_file)
    check_fileimgFile2 = os.path.isfile(imgFile2)# print(check_file)
    check_filedbimg1 = os.path.isfile(dbimg1)# print(check_file)

    if check_fileimgFile1 and check_fileimgFile2 and check_filedbimg1:
        # imgFile1 = "data/ritikimg.jpg"
        # imgFile2 = "data/pawar.jpeg"
        # dbimg1 = "data/app.png"
        # imgFile2 = "data/krish.jpg"

        # database images
        temp1_image = face_recognition.load_image_file(imgFile1)
        temp1_face_encoding = face_recognition.face_encodings(temp1_image)[0]

        temp2_image = face_recognition.load_image_file(imgFile2)
        temp2_face_encoding = face_recognition.face_encodings(temp2_image)[0]

        # temp images (need to verify images)
        db1_image = face_recognition.load_image_file(dbimg1)
        db1_face_encoding = face_recognition.face_encodings(db1_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            temp1_face_encoding,
            temp2_face_encoding
        ]
        known_face_names = [
            "m1",
            "m2"
        ]

        mymatches = face_recognition.compare_faces(known_face_encodings, db1_face_encoding)
        # print(mymatches)

        face_distances = face_recognition.face_distance(known_face_encodings, db1_face_encoding)
        best_match_index = np.argmin(face_distances)
        # if mymatches[best_match_index]:
        #     name = known_face_names[best_match_index]
        #     print(name)

        if face_distances[best_match_index] < 0.6:
            name = known_face_names[best_match_index]
            print(name)
            matchName = name
            deleteFile(imgFile1,imgFile2,dbimg1)
            return name

        else:
            print("Unknown person")
            deleteFile(imgFile1,imgFile2,dbimg1)
            return "Unknown person"
    else:
        return "400"
    

def deleteFile(imgFile1,imgFile2,dbimg1):
    def removfile(file):
        path = os.path.basename(file)
        os.remove(path)

    # dbimg1 = "verify1.jpg"
    filearr = [imgFile1,imgFile2,dbimg1]
    
    check_fileimgFile1 = os.path.isfile(imgFile1)# print(check_file)
    check_fileimgFile2 = os.path.isfile(imgFile2)# print(check_file)
    check_filedbimg1 = os.path.isfile(dbimg1)# print(check_file)

    if check_fileimgFile1:
        removfile(imgFile1)
    if check_fileimgFile2:
        removfile(imgFile2)
    if check_filedbimg1:
        removfile(dbimg1)
    if (not check_fileimgFile1 or not check_fileimgFile2 or not check_filedbimg1):
        print(f"Temp files present")



@app.route('/home')
def index():
    return render_template('myverify.html')
    
    
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
    elif request.method=='GET':
        return render_template('myverify.html')
    return render_template('myverify.html')


@app.route('/userid/<string:id>')
def username(id):
    imgName = f'{id}.jpg'
    # get database images
    storage.child("images").child(imgName).download(filename='down1.jpg',path="/data/downloads")
    storage.child("images").child(imgName).download(filename='down2.jpg',path="/data/downloads")

    # get temp verification images
    timgName = f'{id}.jpg'
    storage.child("temp").child(imgName).download(filename='verify1.jpg',path="/data/downloads")
    
    userid1 = id
    gotRes = recog(userid1)
    goodapiresponse = {
        'status': '200',
        'matched': gotRes
    }
    badapiresponse = {
        'status': '400',
        'matched': gotRes
    }
    if len(gotRes) == 0:
        return jsonify(badapiresponse)
    else:
        return jsonify(goodapiresponse)

# test  /userid/1


@app.route('/video_feed')
def video_feed():
    global userid
    recog(userid)
    return render_template('myverify.html')




if __name__ == '__main__':
    app.run(debug=True)
    
camera.release()
cv2.destroyAllWindows()     