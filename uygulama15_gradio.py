import cv2 as cv
import gradio as gr

# Görüntü boyutlandırma fonksiyonu
def resize_image(image, fx=0.5, fy=0.5):
    # OpenCV, resmi BGR formatında okur, ancak Gradio RGB formatında çalışır.
    # Bu nedenle, renk uzayını dönüştürmemiz gerekiyor.
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    
    # Görüntüyü yeniden boyutlandır
    resized_img = cv.resize(image, None, fx=fx, fy=fy)
    
    # Yeniden boyutlandırılmış resmi RGB formatına geri dönüştür
    resized_img = cv.cvtColor(resized_img, cv.COLOR_BGR2RGB)
    
    return resized_img

# Gradio arayüzü oluşturma
with gr.Blocks() as demo:
    gr.Markdown("# Görüntü Boyutlandırma Uygulaması")
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Resim Yükle", type="numpy")
            fx_slider = gr.Slider(0.1, 2.0, value=0.5, step=0.1, label="Yatay Boyutlandırma Oranı (fx)")
            fy_slider = gr.Slider(0.1, 2.0, value=0.5, step=0.1, label="Dikey Boyutlandırma Oranı (fy)")
            resize_button = gr.Button("Boyutlandır")
        with gr.Column():
            output_image = gr.Image(label="Yeniden Boyutlandırılmış Resim")
            download_button = gr.File(label="Resmi İndir")

    # Boyutlandırma işlemini gerçekleştiren fonksiyon
    def perform_resize(image, fx, fy):
        resized_img = resize_image(image, fx, fy)
        # İndirme için geçici bir dosya oluştur
        temp_file = "resized_image.jpg"
        cv.imwrite(temp_file, cv.cvtColor(resized_img, cv.COLOR_RGB2BGR))
        return resized_img, temp_file

    # Butona tıklandığında çalışacak işlem
    resize_button.click(
        fn=perform_resize,
        inputs=[input_image, fx_slider, fy_slider],
        outputs=[output_image, download_button]
    )

# Uygulamayı başlat
demo.launch()