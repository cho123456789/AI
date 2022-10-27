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
import yolo_detector2
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

file_barcode = "C:\\Users\\h\\Desktop\\yolov5\\yolov5\\img\\4.png"

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


###############   바코드 텐서 값 뽑아오기    ##########################################
def barcheck(bdir):
    if bdir == True:
        img = cv2.imread(file_barcode,cv2.IMREAD_UNCHANGED)    #이미지 부르기
        det = yolo_detector2.detect(img)                                 #이미지 디텍팅
        print(det)
        if det is not None:                                             #디텍팅 될 부분이 있는 지 확인
            nam = det[0][5]                         #훼손 내용 받아오기
            if torch.eq(nam,torch.tensor(0.)):              #1번 책의 경우
                number = 1
            elif torch.eq(nam,torch.tensor(1.)):            #2번 책의 경우
                number = 2
            elif torch.eq(nam,torch.tensor(2.)):            #3번 책의 경우
                number = 3
            image = yolo_detector2.draw_boxes(img, det)                  #디텍팅 된다면 이미지에 그리기
        cv2.imwrite(file_barcode,image)                        #이미지 저장하기
            
    else:
        print("failed")
    return number
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
bucket = storage.bucket()
fbdown(bucket)

bdir = os.path.isfile(file_barcode)
print("number" ,bdir)  # True                               #경로에 파일이 있는 지 확인

# 바코드 인식할때 바코드 번호에 따라서 db 저장문이 달라진다 
number = barcheck(bdir)
print("barcode number",number)

if number == 1:
    def uplist(c_name):
        
        doc_ref = db.collection(u'user').document(u'book1')
        doc_ref.update({    
            u'next' : c_name,
            u'bookname' : "해리포터와 불의잔",
            u'bookwriter' : "조앤콜링"
        })
    
    def litoday():
        doc_ref = db.collection(u'user').document(u'book1')
        doc = doc_ref.get()
        # print(doc.get('today'))
        today = doc.get('today')
        return today

    def linext():
        doc_ref = db.collection(u'user').document(u'book1')
        doc = doc_ref.get()
        # print(doc.get('next'))
        next = doc.get('next')
        return next

    def fincheck(a, b):
        la = len(a)
        lb = len(b)
        if la == lb:
            ch = bmk_check.icheck(a, b)
            if ch == True:
                t1 = '정상입니다. 반납해주세요.'
                doc_ref = db.collection(u'user').document(u'book1')
                doc_ref.update({    
                    u'txt2' : t1
                })
            else:
                t2 = '창구를 확인해주세요.'
                doc_ref = db.collection(u'user').document(u'book1')
                doc_ref.update({    
                    u'txt2' : t2
                })
        elif la < lb:
            t2 = '창구를 확인해주세요.'
            doc_ref = db.collection(u'user').document(u'book1')
            doc_ref.update({    
                u'txt2' : t2
            })
        else:
            t3= '오류입니다. 직원을 불러주세요.'
            doc_ref = db.collection(u'user').document(u'book1')
            doc_ref.update({   
                u'txt2' : t3
            })
    


    dir = os.path.isfile(file_path1)
    print(dir)  # True                  #경로에 파일이 있는 지 확인
    c_name = licheck(dir)

    db = firestore.client()
    uplist(c_name)
    print(c_name)

    today = litoday()
    next = linext()
    fincheck(today, next)               #이전 list와 현재 list 비교해서 안내문구 업로드

if number == 2:
    def uplist(c_name):
        doc_ref = db.collection(u'user').document(u'book2')
        doc_ref.update({    
            u'next' : c_name,
            u'bookname' : "돌이킬수 없는 약속",
            u'bookwriter' : "야쿠마루 가쿠"
        })

    def litoday():
        doc_ref = db.collection(u'user').document(u'book2')
        doc = doc_ref.get()
        # print(doc.get('today'))
        today = doc.get('today')
        return today

    def linext():
        doc_ref = db.collection(u'user').document(u'book2')
        doc = doc_ref.get()
        # print(doc.get('next'))
        next = doc.get('next')
        return next

    def fincheck(a, b):
        la = len(a)
        lb = len(b)
        if la == lb:
            ch = bmk_check.icheck(a, b)
            if ch == True:
                t1 = '정상입니다. 반납해주세요.'
                doc_ref = db.collection(u'user').document(u'book2')
                doc_ref.update({    
                    u'txt2' : t1
                })
            else:
                t2 = '창구를 확인해주세요.'
                doc_ref = db.collection(u'user').document(u'book2')
                doc_ref.update({    
                    u'txt2' : t2
                })
        elif la < lb:
            t2 = '창구를 확인해주세요.'
            doc_ref = db.collection(u'user').document(u'book2')
            doc_ref.update({    
                u'txt2' : t2
            })
        else:
            t3= '오류입니다. 직원을 불러주세요.'
            doc_ref = db.collection(u'user').document(u'book2')
            doc_ref.update({   
                u'txt2' : t3
            })
   
    bucket = storage.bucket()
    fbdown(bucket)
    dir = os.path.isfile(file_path1)
    print(dir)  # True                               #경로에 파일이 있는 지 확인
    c_name = licheck(dir)

    db = firestore.client()
    uplist(c_name)
    print(c_name)

    today = litoday()
    next = linext()

    fincheck(today, next)     #이전 list와 현재 list 비교해서 안내문구 업로드

if number == 3:
    def uplist(c_name):
        doc_ref = db.collection(u'user').document(u'book3')
        doc_ref.update({    
            u'next' : c_name,
             u'bookname' : "불편한 편의점",
            u'bookwriter' : "김호연"
        })

    def litoday():
        doc_ref = db.collection(u'user').document(u'book3')
        doc = doc_ref.get()
        # print(doc.get('today'))
        today = doc.get('today')
        return today

    def linext():
        doc_ref = db.collection(u'user').document(u'book3')
        doc = doc_ref.get()
        # print(doc.get('next'))
        next = doc.get('next')
        return next

    def fincheck(a, b):
        la = len(a)
        lb = len(b)
        if la == lb:
            ch = bmk_check.icheck(a, b)
            if ch == True:
                t1 = '정상입니다. 반납해주세요.'
                doc_ref = db.collection(u'user').document(u'book3')
                doc_ref.update({    
                    u'txt2' : t1
                })
            else:
                t2 = '창구를 확인해주세요.'
                doc_ref = db.collection(u'user').document(u'book3')
                doc_ref.update({    
                    u'txt2' : t2
                })
        elif la < lb:
            t2 = '창구를 확인해주세요.'
            doc_ref = db.collection(u'user').document(u'book3')
            doc_ref.update({    
                u'txt2' : t2
            })
        else:
            t3= '오류입니다. 직원을 불러주세요.'
            doc_ref = db.collection(u'user').document(u'book3')
            doc_ref.update({   
                u'txt2' : t3
            })
   
    bucket = storage.bucket()
    fbdown(bucket)
    dir = os.path.isfile(file_path1)
    print(dir)  # True                               #경로에 파일이 있는 지 확인
    c_name = licheck(dir)

    db = firestore.client()
    uplist(c_name)
    print(c_name)

    today = litoday()
    next = linext()

    fincheck(today, next)     #이전 list와 현재 list 비교해서 안내문구 업로드

