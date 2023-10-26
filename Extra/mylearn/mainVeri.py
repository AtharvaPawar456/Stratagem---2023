import os
import cv2
import face_recognition
import numpy as np


def recog():
    imgFile1 = "data/ritikimg.jpg"
    imgFile2 = "data/pawar.jpeg"
    dbimg1 = "data/app.png"
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
    else:
        print("Unknown person")


recog()

# imgFile1 = "data/ritikimg.jpg"
# imgFile2 = "data/krish.jpg"
# dbimg1 = "data/pawar.jpeg"
# dbimg2 = "data/app.png"