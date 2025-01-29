#Kanallar
import cv2 as cv
img=cv.imread(r'data/satranc3x3.jpg')
b,g,r=cv.split(img)
cv.imshow('Orijinal',img)
cv.imshow('B',b)
cv.imshow('G',g)
cv.imshow('R',r)
cv.waitKey(0)
cv.destroyAllWindows()