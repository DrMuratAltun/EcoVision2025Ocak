# görüntü boyutlandırma
import cv2 as cv

img=cv.imread(r"data/gol_manzarasi.jpeg")
cv.imshow('Orijinal Resim',img)


fx,fy=.5,.5

resized_img=cv.resize(img,None,fx=fx,fy=fy)
cv.imshow('Kucuk Resim',resized_img)
#görüntüyü kaydet
cv.imwrite('data/kucuk_resim.jpeg',resized_img)
cv.waitKey(0)
cv.destroyAllWindows()