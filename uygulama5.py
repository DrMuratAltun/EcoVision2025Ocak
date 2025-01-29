# Kırmızı elmayı yeşile çevir
import cv2 as cv
img_bgr=cv.imread(r'data/elma.jpg')

# orijinali göster
cv.imshow('Orijinal',img_bgr)

b,g,r=cv.split(img_bgr)

# mavi elma 
img_rgb=cv.merge((r,g,b))

# mavi elmayı göster
cv.imshow('Mavi Elma',img_rgb)

# yeşil elma
img_brg=cv.merge((b,r,g))


# yeşil elmayı göster
cv.imshow('Yesil Elma',img_brg)

# sarı elma
img_brr=cv.merge((b,r,r))

#Sarı elmayı göster
cv.imshow('Sari elma',img_brr)

cv.waitKey(0)
cv.destroyAllWindows()