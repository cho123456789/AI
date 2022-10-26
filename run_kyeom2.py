from cgitb import strong
from http import client
from pydoc import cli
import firebase_admin
from firebase_admin import credentials , firestore , storage
import numpy as np
import cv2
from requests import request
import requests as req
import urllib.request
from PIL import Image
from bmk_check import litoday, uplist
import yolo_detector
import os
from tokenize import Name
import torch
import bmk_check

##################  firebase 환경설정 ###############################################
cred = credentials.Certificate('hustar-9eeb8-firebase-adminsdk-alcry-ae50a8362d.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'hustar-9eeb8',
    'storageBucket': 'hustar-9eeb8.appspot.com'
})
##########################################################################################


#### 경로 지정 #########################
## 경로 일일이 바꾸는거 화나니까 경로 여기서 다 지정합니다
## 경로 바꿀시에는  여기만 수정하면됩니다 

firebase_file2 = "C:\\Users\\h\\Desktop\yolov5\\yolov5\\img\\"   
#firebase 이미지 다운로드에 대한 경로 

file_path1  = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\2.png"
file_path2 = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\3.png"
# 경로 및  파일 이미지 확인 디텍팅 실시에 대한 경로 

file_path3 = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\1.png"
# 디렉토리 다운 받은 파일 확인하고 훼손된 부분 리스트 추가에 대한 경로 

###########################################


###############   firebase 이미지 다운로드  ##########################################
def fbdown(bucket):
    ds =bucket.list_blobs(prefix='my_folder/')
    print('bucket'.__len__())
    count = 0 
    for blob in ds:
        if(not blob.name.endswith("/")):
            count+=1
            print(f'Downloading file [{blob.name}]',count) 
            file2 = firebase_file2 +str(count)+".png"
            #file = "C:\\Users\\h\\Desktop\\yolov5\\img\\"+str(count)+".png"
            print(file2)
            blob.download_to_filename(file2)
            if count == 5:
                break
####################################################################################
            

###############   경로 확인 및 이미지 디텍팅과 훼손 리스트 생성 ############################
def licheck(dir):
    if dir == True:
        img = cv2.imread(file_path1,cv2.IMREAD_UNCHANGED)    #이미지 부르기
        det = yolo_detector.detect(img)                                 #이미지 디텍팅
        print(det)
        if det is not None:                                             #디텍팅 될 부분이 있는 지 확인
            c_name = bmk_check.apdam(det)
            image = yolo_detector.draw_boxes(img, det)                  #디텍팅 된다면 이미지에 그리기
        cv2.imwrite(file_path2,image)                        #이미지 저장하기
        #cv2.imshow('my window',image) #별도의 창으로 띄우기
        bucket = storage.bucket()
    #########################   바꿀 여지 존재  ################################
        blob = bucket.blob('my_folder/3.png')                           #들고 올 이미지가 있는 파이어베이스 주소
    ############################################################################
        blob.upload_from_filename(filename=file_path2)       #저장 할 주소
            
    else:
        print("failed")
    return c_name
####################################################################################


#################   아래에서 collection, document 이름 변경 ##########################

    
###############   파이어베이스에 현재(새로운) list 넣기     ############################
def uplist(c_name):
    doc_ref = db.collection(u'user').document(u'test2')
    doc_ref.update({    
        u'next' : c_name
    })
####################################################################################

    
###############   today list 다운받기     ########################################
def litoday():
    doc_ref = db.collection(u'user').document(u'test2')
    doc = doc_ref.get()
    # print(doc.get('today'))
    today = doc.get('today')
    return today
####################################################################################


###############   next list 다운받기     ########################################
def linext():
    doc_ref = db.collection(u'user').document(u'test2')
    doc = doc_ref.get()
    # print(doc.get('next'))
    next = doc.get('next')
    return next
####################################################################################


###############   이전 list와 현재 list를 비교해서 안내문구 업로드  ############################
def fincheck(a, b):
    la = len(a)
    lb = len(b)
    if la == lb:
        ch = bmk_check.icheck(a, b)
        if ch == True:
            t1 = '정상입니다. 반납해주세요.'
            doc_ref = db.collection(u'user').document(u'test')
            doc_ref.update({    
                u'txt2' : t1
            })
        else:
            t2 = '창구를 확인해주세요.'
            doc_ref = db.collection(u'user').document(u'test')
            doc_ref.update({    
                u'txt2' : t2
            })
    elif la < lb:
        t2 = '창구를 확인해주세요.'
        doc_ref = db.collection(u'user').document(u'test')
        doc_ref.update({    
            u'txt2' : t2
        })
    else:
        t3= '오류입니다. 직원을 불러주세요.'
        doc_ref = db.collection(u'user').document(u'test')
        doc_ref.update({   
            u'txt2' : t3
        })
####################################################################################
####################################################################################
####################################################################################

        

##############    firebase 이미지 다운로드  ###########################################
###########    Android에서 찍어서 -> firebase 올려서 -> python으로 다운로드 ###########

bucket = storage.bucket()

#############  fireabase 이미지 다운로드 #########################################



###########  경로 및  파일 이미지 확인 디텍팅 실시  ################################

#file_path = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\2.png"
#file_path2 = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\3.png"
dir = os.path.isfile(file_path1)
print(dir)  # True                               #경로에 파일이 있는 지 확인
c_name = bmk_check.licheck(dir)

######################  경로 및  파일 이미지 확인 디텍팅 실시 ###########################



#img = cv2.imread("C:/Users/HUSTAR09/Desktop/book/try/images/img001.jpg",cv2.IMREAD_UNCHANGED)



####### 파이어베이스에 c_name 즉 새로운 리스트 넣기 ######################################

db = firestore.client()
bmk_check.uplist(c_name)

##########################################################################################



########## 파이어 베이스에 넣은 리스트 불러오기 ###########################################

today = bmk_check.litoday()
next = bmk_check.linext()

bmk_check.fincheck(today, next)     #이전 list와 현재 list 비교해서 안내문구 업로드

################# 파이어 베이스에 넣은 리스트 불러오기 #########################################




###  각 해당하는 기능들을 함수로 구현해서 메인에서 함수선언으로 돌아가게 하고싶어요 ㅠㅠ.... ###     
##   수겸아 부탁해...
#  