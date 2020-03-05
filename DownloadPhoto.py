#!/usr/bin/env python
# coding: utf-8

# In[1]:


import firebase_admin
import re
import json
import time
import urllib.request
import os
from firebase_admin import credentials
from firebase_admin import db


# In[2]:


#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('myKey.json') # 해당 파일은 쥬피터 내의 현재 python 파일과 같은 경로에 저장
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://aicctv-8f5ac.firebaseio.com/"
})


# In[3]:


ID = "00gpwls00" # 이용자마다 다르게 코딩해야 하는 부분
ref = db.reference(ID+"/PhotoLink") #db 위치 지정


# In[ ]:


while True: # 무한 반복문
    
    dic=ref.get() # dict object
    tmp_str=json.dumps(dic, ensure_ascii=False)[1:-1] # 한글을 포함해 string으로 변환 후 맨 앞과 뒤의 {} 제거
    tmp=re.sub(r': {[^}]*}', '', tmp_str) #  쉼표와 이름을 제외하고 모든 문자 삭제
    people=tmp.split(", ") # 사진에 등록된 사람들 이름만 추출   
    
    for i in range (len(people)): # 얼굴이 등록된 사람 수 만큼 실행
        person_ref=db.reference(ID+"/PhotoLink/"+people[i][1:-1]) # 쉼표를 제거해 레퍼런스 생성
        DownCount_ref=person_ref.child('DownCount') # 컴퓨터에 다운로드 된 파일 레퍼런스
        UpdateCount_ref=person_ref.child('UpdateCount') # 데이터베이스에 업로드된 파일 레퍼런스
        
        DownCount=DownCount_ref.get()
        UpdateCount=UpdateCount_ref.get()
        
        if (DownCount!=UpdateCount) : # 업데이트를 해야하는 경우 (다운로드가 필요한 경우)
            outpath="C:/"+ID+"/"+people[i][1:-1]+"/"
            # 위의 outpath 경로가 존재하지 않을 경우, 경로를 생성함
            if not os.path.isdir(outpath):
                os.makedirs(outpath)
            # 배열로 파일명을 모두 split해서 저장
            tmp_photoLink=json.dumps(person_ref.get(), ensure_ascii=False)[2:-1]
            photoLink=re.sub(r': "[^"]*",', '', tmp_photoLink)
            photo_array=photoLink.split('\" \"')

            for j in range (DownCount+1, UpdateCount+1) : # 두 수의 차이만큼 반복 필요
                file_name=photo_array[j-1]
                url=person_ref.child(file_name).get()
                urllib.request.urlretrieve(url, outpath+file_name+".png") # 다운로드
                DownCount+=1 # 데이터베이스에 업데이트 하기 위해서 다운로드 받으며 체크
            DownCount_ref.set(DownCount) # 다운로드를 모두 완료한 후 변수값을 변경
            
    time.sleep(60); # 60초에 한번씩만 확인 및 다운로드


# In[ ]:




