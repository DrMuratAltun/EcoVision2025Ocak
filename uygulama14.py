# Görsel kırpma
import cv2 as cv

img=cv.imread(r"data/gol_manzarasi.jpeg")

cv.imshow('Orijinal Resim',img)

h,w=img.shape[:2]

baslangic_orani=.25
bitis_orani=.75
start_row,start_col=int(h*baslangic_orani),int(w*baslangic_orani)
end_row,end_col=int(h*bitis_orani),int(w*bitis_orani)
cropped_img=img[start_row:end_row,start_col:end_col]
cv.imshow('Gorsel Kırpma',cropped_img)
cv.waitKey(0)
cv.destroyAllWindows()