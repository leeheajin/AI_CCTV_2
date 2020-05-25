import time
from subprocess import call
import picamera
import json
import pyrebase
from firebase import firebase


config={
    "apiKey": "AIzaSyDAA2XR7x3iNsx9cQdhH6FVw8qY3Q3grFU", # webkey
    "authDomain": "aicctv-8f5ac", # projectID
    "databaseURL": "https://aicctv-8f5ac.firebaseio.com/", 
    "storageBucket": "aicctv-8f5ac.appspot.com", # storageURL
    "serviceAccount": "/home/pi/Desktop/myKey.json"
}
 
firebase=pyrebase.initialize_app(config)

storage=firebase.storage()
db=firebase.database()

filename = "20200525_134618"
db.child("00gpwls00/VideoLink/"+filename).remove()
storage.delete("00gpwls00/Video/"+filename+".mp4")