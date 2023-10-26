import pyrebase
import random

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
db = firebase.database()

val = "2"


def GenRandomToken():
    def randN(N):
        min = pow(10, N-1)
        max = pow(10, N) - 1
        return random.randint(min, max)
    tokenres = randN(5)
    # print(tokenres)
    return tokenres

# db.child("patients").child("userid").child(val).child("id").set(val)
# db.child("patients").child("userid").child(val).child("userStatus").set("200")
# db.child("patients").child("userid").child(val).child("token").set("456")


db.child("patients").child("userid").child(val).child("id").set(val)
db.child("patients").child("userid").child(val).child("userStatus").set("400")
db.child("patients").child("userid").child(val).child("token").set(GenRandomToken())


users = db.child("patients").child("userid").child(val).get()
print("id", users.val()["id"])
print("userStatus", users.val()["userStatus"])
print("userStatus", users.val()["token"])