#Dosya uzantısı değiştirme
import cv2 as cv
img=cv.imread(r'data\elma.jpg')

# orijinali göster
cv.imshow('Orijinal',img)

#farklı şekilde dosyayı kaydet
try:
    cv.imwrite('data\elma.png',img)
    print('Dosya kaydedildi')
except:
    print('Dosya kaydedilemedi')

cv.waitKey(0)
cv.destroyAllWindows()