import cv2 as cv
import numpy as np

# Görüntüyü yükle
img_bgr = cv.imread(r'data\siyah_sacli3.jpg')

if img_bgr is None:
    print("Görüntü yüklenemedi!")
    exit()

# HSV renk uzayına çevir (Hue değerleri daha kolay manipüle edilebilir)
img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)

# Siyah tonları için renk aralığı (Hue, Saturation, Value)
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 40])  # Value <= 40 koyu renkleri seçer

# Maske oluştur
mask = cv.inRange(img_hsv, lower_black, upper_black)

# Kızıl rengi belirle (BGR formatında)
kizil_renk = [0, 0, 200]  # Koyu kızıl tonu

# Maskelenmiş alanları kızıla boya
img_modified = img_bgr.copy()
img_modified[mask > 0] = kizil_renk

# Sonuçları göster
cv.imshow('Orijinal', img_bgr)
cv.imshow('Kizil Sac', img_modified)
cv.waitKey(0)
cv.destroyAllWindows()
