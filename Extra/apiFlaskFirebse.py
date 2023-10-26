import pyrebase
import os

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
my_img1 = "1.jpg"
my_img2 = "2.jpg"
# img2 = "app-ring.pngf2338300-9a87-4b62-a793-3781a95781bf"
# img2 = "1"


# uid = "1"
# uimgName = f'{uid}.jpg'


# Upload Image
# storage.child("images").child(my_img1).put(my_img1)
# storage.child("temp").child(uimgName).put(my_img2)



# storage.child("temp").put(dbImg)
# print(f"data/{os.path.basename(my_img1)}")
# Download Image
# storage.child("images").child(my_img1).download(filename='down1.jpg',path=os.path.basename(my_img1))
# customePath = f"data/{os.path.basename(my_img1)}"
# storage.child("images").child(my_img1).download(filename='down1.jpg',path="/data/downloads")

# id = "3"
# imgName = f'{id}.jpg'
# value = storage.child("images").child(imgName).download(filename='2.jpg',path="/data/downloads")
# print(value)

# Temp img 
# tid = "1"
# timgName = f'{tid}.jpg'
# value = storage.child("temp").child(timgName).download(filename='verify1.jpg',path="/data/downloads")

# dbimg1 = "down2.jpg"
# path = os.path.basename(dbimg1)
# print(path)
# os.remove(path)
# print(f"Temp files has been removed successfully")


# check_file = os.path.isfile(dbimg1)
# print(check_file)


imgFile1 = "shots/1.jpg"
filenamefb = "1.jpg"
check_fileimgFile1 = os.path.isfile(imgFile1)# print(check_file)
if check_fileimgFile1:
    print("file uploaded on firebase")
    storage.child("temp").child(filenamefb).put(imgFile1)