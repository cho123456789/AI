import yolo_detector2
import cv2
import os

file_path = "D:/yolov5/img/1.jpg"

dir = os.path.isfile(file_path)
print(dir)  # True                               #경로에 파일이 있는 지 확인

if dir == True:
    img = cv2.imread("D:/yolov5/img/1.jpg",cv2.IMREAD_UNCHANGED) #이미지 부르기
    det = yolo_detector2.detect(img) #이미지 디텍팅
    print(det)
    if det is not None: #디텍팅 될 부분이 있는 지 확인
        image = yolo_detector2.draw_boxes(img, det)  #디텍팅 된다면 이미지에 그리기
    cv2.imwrite("D:/yolov5/img/1.jpg",image) #이미지 저장하기
    #cv2.imshow('my window',image) #별도의 창으로 띄우기
    cv2.waitKey()

else:
    print("failed")

