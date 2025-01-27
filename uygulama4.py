# Farklı okuma modları
import cv2 as cv
img_path=r'D:\Goruntuis2025Ocak\data\yesil_elma.jpg'

#renkli okuma
img_color=cv.imread(img_path,1) # 1 yerine IMREAD_COLOR

#siyah beyaz okuma
img_gray=cv.imread(img_path,0) # 0 yerine IMREAD_GRAYSCALE

cv.imshow('Renkli Elma',img_color)
cv.imshow('Siyah Beyaz Elma',img_gray)


cv.waitKey(0)
cv.destroyAllWindows()