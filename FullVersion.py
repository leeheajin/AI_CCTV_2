import time
import picamera
import json
import pyrebase
from firebase import firebase

config={
    "apiKey": "AIzaSyDAA2XR7x3iNsx9cQdhH6FVw8qY3Q3grFU", # webkey
    "authDomain": "aicctv-8f5ac", # projectID
    "databaseURL": "https://aicctv-8f5ac.firebaseio.com/", 
    "storageBucket": "aicctv-8f5ac.appspot.com" # storageURL
}

firebase=pyrebase.initialize_app(config)
uploadfile="/home/pi/" # camera
storage=firebase.storage()
db=firebase.database()

while True :
    now=time.localtime()
    filename="%04d%02d%02d_%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    uploadfile="/home/pi/Desktop/"+filename+".h264"
    
    with picamera.PiCamera() as camera: # make a video file
        camera.resolution = (240, 240) # video size
        camera.start_recording(output=filename+".h264") # now time is used to file name
        camera.wait_recording(100) # video file time length
        camera.stop_recording() # stop film

    storage.child("1/Video/"+filename+".h264").put(uploadfile)
    print(filename+".h264 done file upload!")
          
    fileUrl=storage.child("1/Video/"+filename+".h264").get_url(1) # 0: storage url, 1: download url
    db.child("1/VideoLink/"+filename).set(fileUrl)
    
    print(filename+".h264 done url push!")