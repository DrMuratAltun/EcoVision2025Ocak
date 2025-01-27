import cv2 as cv
# imread fonksiyonu

img=cv.imread('D:\Goruntuis2025Ocak\data\satranc3x3.jpg')
#print(img[300:400,:])
# ekranda göster imshow
cv.imshow('Satranc Tahtasi',img)
cv.waitKey(0)
cv.destroyAllWindows()