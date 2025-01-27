import cv2 as cv

#resmi oku
img=cv.imread(r'D:\Goruntuis2025Ocak\data\yesil_elma.jpg')

#resmi ekranda göster
cv.imshow('Yesil Elma',img)
#Görüntü özelliklerini al
# yükseklik ve genişlik
print('yükseklik, genişlik ve kanal sayısı',img.shape)
print('yükseklik',img.shape[0])
print('genişlik',img.shape[1])
print('kanal sayısı',img.shape[2])
print (f'Veri türü: {img.dtype}') 
#klavyeden bir tuşa basılmasını bekle
cv.waitKey(0)
#tüm pencereleri kapat
cv.destroyAllWindows()