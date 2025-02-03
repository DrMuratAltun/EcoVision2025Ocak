import cv2 as cv

# Resmi yükle
img = cv.imread(r'data/monalisa.jpg')
cv.imshow('Orijinal Resim', img)
print(f'Görselin boyutları: genişlik {img.shape[1]}, yükseklik {img.shape[0]}')

# Kırmızı çizgiler ekle
cv.line(img, (0, 0), (533, 719), (0, 0, 255), thickness=3)
cv.line(img, (533, 0), (0, 719), (0, 0, 255), thickness=3)

# İçini beyaz olan bir dikdörtgen ekle
cv.rectangle(img, (140, 300), (400, 400), (255, 255, 255), thickness=cv.FILLED)  # Beyaz dolgu

# Yazı için arka plan rengi (beyaz dikdörtgen)
cv.rectangle(img, (140, 340), (400, 380), (255, 255, 255), thickness=cv.FILLED)  # Yazı arka planı

# Yazı ekle
cv.putText(img, 'Fake Mona Lisa', (150, 370), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Siyah renkli yazı

# Sonucu göster
cv.imshow('Kırmızı Çizgi ve Yazı', img)
cv.waitKey(0)
cv.destroyAllWindows()