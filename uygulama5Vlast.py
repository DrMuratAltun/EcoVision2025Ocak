import cv2 as cv
import numpy as np

# Fare olayları için global değişkenler
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1

def mouse_callback(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            fx, fy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y

# Görüntüyü yükle
img_bgr = cv.imread(r'data\siyah_sacli3.jpg')
if img_bgr is None:
    print("Görüntü yüklenemedi!")
    exit()

# Fare etkileşimini başlat
cv.namedWindow('Secim Yapin')
cv.setMouseCallback('Secim Yapin', mouse_callback)

# Kullanıcı seçim yapana kadar bekle
while True:
    temp_img = img_bgr.copy()
    if ix != -1 and fx != -1:
        cv.rectangle(temp_img, (ix, iy), (fx, fy), (0,255,0), 2)
    cv.imshow('Secim Yapin', temp_img)
    
    # SPACE tuşuyla onayla
    if cv.waitKey(1) == 32:
        break

# ROI (Seçilen Alan) koordinatları
x1, y1 = min(ix, fx), min(iy, fy)
x2, y2 = max(ix, fx), max(iy, fy)

# ROI maskesi oluştur
roi_mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)
roi_mask[y1:y2, x1:x2] = 255

# Renk dönüşümü parametreleri
SIYAH_ESIK = 80
KIZIL_ARTIS = 1.8

# 1. Tüm görüntüde siyah maskesi
total_channels = img_bgr.sum(axis=2)
color_mask = total_channels < SIYAH_ESIK * 3

# 2. Kombine maske (ROI + Renk)
final_mask = cv.bitwise_and(roi_mask, color_mask.astype(np.uint8))

# 3. Dönüşümü uygula
img_modified = img_bgr.copy()
for y in range(y1, y2):
    for x in range(x1, x2):
        if final_mask[y, x]:
            B, G, R = img_bgr[y, x]
            orijinal_parlaklik = (B + G + R) // 3
            yeni_R = min(255, int(orijinal_parlaklik * KIZIL_ARTIS))
            yeni_B = max(0, B - int((yeni_R - R) * 0.3))
            yeni_G = max(0, G - int((yeni_R - R) * 0.2))
            img_modified[y, x] = [yeni_B, yeni_G, yeni_R]

# Sonuçları göster
cv.imshow('Orijinal', img_bgr)
cv.imshow('Kizil Sac (Secimli)', img_modified)
cv.waitKey(0)
cv.destroyAllWindows()