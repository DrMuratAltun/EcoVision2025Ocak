import cv2 as cv
import gradio as gr

# Görsel kırpma fonksiyonu
def crop_image(image, baslangic_orani=0.25, bitis_orani=0.75):
    # OpenCV, resmi BGR formatında okur, ancak Gradio RGB formatında çalışır.
    # Bu nedenle, renk uzayını dönüştürmemiz gerekiyor.
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    
    h, w = image.shape[:2]
    
    # Kırpma koordinatlarını hesapla
    start_row, start_col = int(h * baslangic_orani), int(w * baslangic_orani)
    end_row, end_col = int(h * bitis_orani), int(w * bitis_orani)
    
    # Resmi kırpa
    cropped_img = image[start_row:end_row, start_col:end_col]
    
    # Kırpılmış resmi RGB formatına geri dönüştür
    cropped_img = cv.cvtColor(cropped_img, cv.COLOR_BGR2RGB)
    
    return cropped_img

# Resim yükleme işlemini gerçekleştiren fonksiyon
def display_image(image):
    return image

# Gradio arayüzü oluşturma
with gr.Blocks() as demo:
    gr.Markdown("# Görsel Kırpma Uygulaması")
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Yüklenecek Resim", type="numpy")
            #uploaded_image = gr.Image(label="Yüklenen Resim", interactive=False)
            baslangic_orani_slider = gr.Slider(0, 1, value=0.25, label="Başlangıç Oranı")
            bitis_orani_slider = gr.Slider(0, 1, value=0.75, label="Bitiş Oranı")
            crop_button = gr.Button("Kırp")
        with gr.Column():
            output_image = gr.Image(label="Kırpılmış Resim")

    # Resim yüklendiğinde otomatik olarak göster
    #input_image.change(fn=display_image, inputs=input_image, outputs=uploaded_image)

    # Butona tıklandığında çalışacak işlem
    crop_button.click(fn=crop_image, inputs=[input_image, baslangic_orani_slider, bitis_orani_slider], outputs=output_image)

# Uygulamayı başlat
demo.launch()