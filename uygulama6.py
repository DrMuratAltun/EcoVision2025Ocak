# Kırmızı elmayı yeşile çevir
import cv2 as cv
img_bgr=cv.imread(r'data\kirmizi_ferrari.jpg')

# orijinali göster
cv.imshow('Orijinal',img_bgr)

b,g,r=cv.split(img_bgr)

# mavi ferrari
img_rgb=cv.merge((r,g,b))

# mavi ferrari göster
cv.imshow('Mavi Ferrari',img_rgb)

# yeşil ferrari
img_brg=cv.merge((b,r,g))


# yeşil ferrari göster
cv.imshow('Yesil Ferrari',img_brg)

# sarı ferrari
img_brr=cv.merge((b,r,r))

#Sarı ferrari göster
cv.imshow('Sari Ferrari',img_brr)

cv.waitKey(0)
cv.destroyAllWindows()