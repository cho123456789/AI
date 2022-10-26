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
import torch
import os




###############   디텍팅된 사진에서 텐서 값 뽑아오기    ##########################################
def apdam(det):
    c_name = []
    for i in range(len(det)):                   #디텍팅된 항목 수만큼 반복
        per = det[i].tolist()
        pen = per[4]                            #정확도 받아오기
        nam = det[i][5]                         #훼손 내용 받아오기
        if pen >= 0.1:                          #정확도가 일정 이상이면 append
            if torch.eq(nam,torch.tensor(1.)):
                c_name.append("notch")
            elif torch.eq(nam,torch.tensor(2.)):
                c_name.append("ripped")
            elif torch.eq(nam,torch.tensor(3.)):
                c_name.append("spot")
            elif torch.eq(nam,torch.tensor(5.)):
                c_name.append("wornout")
        else:
            continue
    return c_name
####################################################################################


#############   a와 b를 비교해서 늘어난 훼손 내용 확인 -> 추가된 내역만 리스트로 반환 ##############
def check(a, b):
    a.sort()
    b.sort()
    c = b
    for i in range(len(a)):         # c에 b를 넣어서 a와 b가 겹치는 부분을 c에서 삭제
        if a[i] in b:
            c.remove(a[i])
    return c
####################################################################################


###############   추가된 훼손 내용과 횟수를 확인하는 함수   ##########################################
def ncheck(b):
    d = []
    for i in range(len(b)):         # a와 b에서 차이가 발생한 것 중 중복 제거
        if b[i] not in d:
            d.append(b[i])
        else:
            continue
    for j in range(len(d)):         # 각 훼손마다 몇 번 발생했는지 확인
        print('%s가 %d회 감지되었습니다.' % (d[j], b.count(d[j])))
####################################################################################
        

###############   길이가 같은 경우 a가 b에 포함되는지 확인하는 함수 ############################
def icheck(a, b):
    a.sort()
    b.sort()
    c = b
    for i in range(len(a)):         # a와 b에서 내용의 차이가 존재하는지 확인
        if a[i] in b:
            c.remove(a[i])          # a와 b가 같다면 True 반환
        else:                       # a와 b가 다르면 False 반환
            continue
    if c is None:
        return True
    else:
        return False
####################################################################################
    

    
