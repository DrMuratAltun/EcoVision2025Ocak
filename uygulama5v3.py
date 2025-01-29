# Kırmızı elmayı yeşile çevir
import cv2 as cv
img_bgr=cv.imread(r'data\siyah_sacli3.jpg')

# orijinali göster
cv.imshow('Orijinal',img_bgr)

b,g,r=cv.split(img_bgr)

# mavi yüz 
img_rgb=cv.merge((r,g,b))

# mavi yüz göster
cv.imshow('Mavi Elma',img_rgb)

# yeşil yüz
img_brg=cv.merge((b,r,g))


# yeşil yüz göster
cv.imshow('Yesil Elma',img_brg)

# sarı yüz
img_brr=cv.merge((b,r,r))

#Sarı yüz göster
cv.imshow('Sari elma',img_brr)

cv.waitKey(0)
cv.destroyAllWindows()