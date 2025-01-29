import cv2 as cv

# Kamera aç
cap=cv.VideoCapture(0) # 0 : varsayılan kamera
while True:
    ret,frame=cap.read()
    cv.imshow('Kamera',frame)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
    gray_frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    hsv_img=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    flipped=cv.flip(frame,1) # 0: x ekseninde, 1: y ekseninde, -1: hem x hem y ekseninde
    
    cv.imshow('Flipped',flipped)
    cv.imshow('HSV',hsv_img)
    cv.imshow('Gray',gray_frame)