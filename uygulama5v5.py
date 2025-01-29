import cv2 as cv
import numpy as np

img_bgr = cv.imread(r'data\siyah_sacli3.jpg')

if img_bgr is None:
    print("Görüntü yüklenemedi!")
    exit()

# Siyahı hedefleme parametreleri
SIYAH_ESIK = 30.0       # Ne kadar koyu renkler seçilecek (0-255)
KIZIL_ARTIS = 2.5    # Kızıl tonunun şiddeti (1.5-3.0 arası deneyin)

# 1. Siyahı maskeleme (BGR toplamına göre)
total_channels = img_bgr.sum(axis=2)
mask = total_channels < SIYAH_ESIK * 3  # 3 kanal olduğu için

# 2. Orijinal parlaklığı koruyarak kızıla dönüştürme
img_modified = img_bgr.copy()

# Maskeli pikseller için işlem:
for y in range(img_bgr.shape[0]):
    for x in range(img_bgr.shape[1]):
        if mask[y, x]:
            B, G, R = img_bgr[y, x]
            
            # Orijinal parlaklık (0-255)
            orijinal_parlaklik = (B + G + R) / 3
            
            # Kızıl rengi parlaklığa göre ölçeklendir
            yeni_R = min(255, int(orijinal_parlaklik * KIZIL_ARTIS))
            
            # Mavi ve yeşili azaltarak denge sağla
            yeni_B = max(0, B - int((yeni_R - R) * 0.3))
            yeni_G = max(0, G - int((yeni_R - R) * 0.2))
            
            img_modified[y, x] = [yeni_B, yeni_G, yeni_R]

# Sonuçları göster
cv.imshow('Orijinal', img_bgr)
cv.imshow('Kizil Sac (BGR)', img_modified)
cv.waitKey(0)
cv.destroyAllWindows()
