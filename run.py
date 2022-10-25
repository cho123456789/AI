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
import yolo_detector
import os
from tokenize import Name
import torch
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



###
##############    firebase 이미지 다운로드  ###########################################
bucket = storage.bucket()
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
#############  fireabase 이미지 다운로드 #########################################



###########  경로 및  파일 이미지 확인 디텍팅 실시  ################################

#file_path = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\2.png"
#file_path2 = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\3.png"
dir = os.path.isfile(file_path1)
print(dir)  # True                               #경로에 파일이 있는 지 확인

if dir == True:
    img = cv2.imread(file_path1,cv2.IMREAD_UNCHANGED) #이미지 부르기
    det = yolo_detector.detect(img) #이미지 디텍팅
    print(det)
    if det is not None: #디텍팅 될 부분이 있는 지 확인
        image = yolo_detector.draw_boxes(img, det)  #디텍팅 된다면 이미지에 그리기
    cv2.imwrite(file_path2,image) #이미지 저장하기
    #cv2.imshow('my window',image) #별도의 창으로 띄우기
    bucket = storage.bucket()
    blob = bucket.blob('my_folder/3.png') #들고 올 이미지가 있는 파이어베이스 주소
    blob.upload_from_filename(filename=file_path2) #저장 할 주소
           
else:
    print("failed")
######################  경로 및  파일 이미지 확인 디텍팅 실시 ###########################



#img = cv2.imread("C:/Users/HUSTAR09/Desktop/book/try/images/img001.jpg",cv2.IMREAD_UNCHANGED)



#######################   디렉토리 다운 받은 파일 확인하고 훼손된 부분 리스트 추가 #######################
#file_path = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\1.png"
img2 = cv2.imread(file_path3,cv2.IMREAD_UNCHANGED)
det = yolo_detector.detect(img2)
print(det)

if dir == True:  
    # 디렉토리 다운 받은 파일 확인하고 훼손된 부분 리스트 추가 
    
    img = cv2.imread(file_path3,cv2.IMREAD_UNCHANGED) #이미지 부르기
    det = yolo_detector.detect(img) #이미지 디텍팅
    print(det)
    if det is not None: #디텍팅 될 부분이 있는 지 확인
        lend = len(det)             #det 길이 받아오기
        c_name = []
        cnt = 0
        while True:
            if cnt == lend:         #카운트가 det 길이와 같으면 탈출
                break
            else:
                per = det[cnt].tolist()
                pen = per[4]        #해당 카운트의 정확도를 받음
                nam = det[cnt][5]   #해당 카운트의 클래스를 받음
                if pen >= 0.5:      #정확도가 0.7 이상인 경우에만 클래스 추가
                    if torch.eq(nam,torch.tensor(0.)):
                        c_name.append("notch")
                    elif torch.eq(nam,torch.tensor(1.)):
                        c_name.append("ripped")
                    elif torch.eq(nam,torch.tensor(2.)):
                        c_name.append("spot")
                    elif torch.eq(nam,torch.tensor(3.)):
                        c_name.append("wornout")
                    cnt += 1
                else:               #정확도가 0.7 미만인 경우
                    cnt += 1        #카운트를 올리고 while문 다시 돌기
                    continue
        image = yolo_detector.draw_boxes(img, det)  #디텍팅 된다면 이미지에 그리기
    cv2.imwrite(file_path3,image) #이미지 저장하기
    #cv2.imshow('my window',image) #별도의 창으로 띄우기

#c_name이 아래 코드에서 리스트 b에 해당하는 내용-현재 찍은 사진에서 훼손 내역-인데
#해당 내용을 파이어베이스 데이터베이스로 올라가는 코드를 못 짬
 

else:
    print("failed")
#######################   디렉토리 다운 받은 파일 확인하고 훼손된 부분 리스트 추가 #######################


"""
훼손 내역 확인 코드
# #a와 b를 비교해서 늘어난 훼손 내용을 확인하는 함수 -> 추가된 내역만 리스트로 반환
# def check(a, b):
#     a.sort()
#     b.sort()
#     c = b
#     for i in range(len(a)):
#         if a[i] in b:
#             c.remove(a[i])
#     return c

# #추가된 훼손 내용과 횟수를 확인하는 함수
# def ncheck(b):
#     d = []
#     for i in range(len(b)):
#         if b[i] not in d:
#             d.append(b[i])
#         else:
#             continue
#     for j in range(len(d)):
#         print('%s가 %d회 감지되었습니다.' % (b[j], b.count(b[j])))

#a = ['notch', 'spot', 'wornout', 'wornout']
#db = firestore.client()
#doc_ref  = db.collection(u'user').document(u'test')
#doc_ref.update({    # 웹서버 데이터 쓰기
#    u'txt' : a
#})
"""



####### 파이어베이스에 c_name 즉 새로운 리스트 넣기 ######################################
db = firestore.client()
doc_ref  = db.collection(u'user').document(u'test2')
doc_ref.update({    
    u'next' : c_name
})
##########################################################################################



########## 파이어 베이스에 넣은 리스트 불러오기 ###########################################
doc_ref = db.collection(u'user').document(u'test2')
doc = doc_ref.get()
print(doc.get('today'))
print(doc.get('next'))

today = doc.get('today')
next = doc.get('next')

"""
이 부분은 나중에 파이어베이스 데이터베이스에서 리스트를 받아오는 걸로 변경해야 됨
a = ['notch', 'spot', 'wornout', 'wornout']
a1 = ['notch', 'spot', 'wornout', '123']
b = ['notch', 'notch', 'spot', 'wornout', 'wornout', 'wornout', 'wornout']  
"""

if (c_name is None):
    print('정보가 없습니다.')
else:
    if len(today) == len(c_name):
        t1 = '정상입니다. 반납해주세요.'
        doc_ref = db.collection(u'user').document(u'test')
        doc_ref.update({    
            u'txt2' : t1
        })
    elif len(today) < len(c_name):
        t2 = '창구를 확인해주세요.'
        # dams = check(a, c_name)
        # ncheck(dams)
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

### 파이어 베이스에 넣은 리스트 불러오기 ##1111111