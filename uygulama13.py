# Pixel manipülasyonu yaparak resim üzerinde işlemler yapma
import cv2 as cv
import numpy as np

img=cv.imread(r"data/yesil_elma.jpg")

# görüntü boyut bilgileri
height, width = img.shape[:2]

print (f'Görselin boyutları:genişlik {width}, yükseklik {height}')

# resmin ortasında beyaz bir kare oluştur
kare_boyut=50
baslangic_x=int((width/2)-(kare_boyut/2))
baslangic_y=int((height/2)-(kare_boyut/2))

for y in range(baslangic_y,baslangic_y+kare_boyut):
    for x in range(baslangic_x,baslangic_x+kare_boyut):
        img[y,x]=(255,255,255)

cv.imshow('Beyaz Kare',img)
cv.waitKey(0)
cv.destroyAllWindows()