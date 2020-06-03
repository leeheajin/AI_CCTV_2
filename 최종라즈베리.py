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
    "storageBucket": "aicctv-8f5ac.appspot.com" # storageURL
}
 
firebase=pyrebase.initialize_app(config)

uploadfile="/home/pi/" # camera

storage=firebase.storage()

db=firebase.database()

while True :

    now=time.localtime()
    filename="%04d%02d%02d_%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    uploadfile="/home/pi/Desktop/"+filename+".mp4"

    with picamera.PiCamera() as camera: # make a video file
        camera.resolution = (240, 240) # video size
        camera.start_recording(output=filename+".h264") # now time is used to file name
        camera.wait_recording(60) # video file time length
        camera.stop_recording() # stop film
        
        command = "MP4Box -add " + filename+".h264" + " " + filename+".mp4"
        call([command], shell=True)
        print("\r\nRasp_Pi => Video Converted! \r")

 

    storage.child("00gpwls00/Video/"+filename+".mp4").put(uploadfile)
    print(filename+".mp4 done file upload!")
    fileUrl=storage.child("00gpwls00/Video/"+filename+".mp4").get_url(1) # 0: storage url, 1: download url
    db.child("00gpwls00/VideoLink/"+filename).set(fileUrl)
    db.child("00gpwls00/VideoLink/Update").set(filename)
    
    print(filename+".mp4 done url push!")