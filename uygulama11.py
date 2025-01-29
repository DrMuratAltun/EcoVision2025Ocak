import cv2
import numpy as np
import gradio as gr

# Gelişmiş Filtre Fonksiyonları
def apply_sepia(frame):
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])
    return cv2.transform(frame, sepia_filter).clip(0, 255).astype(np.uint8)

def apply_emboss(frame):
    kernel = np.array([[-2, -1, 0], 
                      [-1, 1, 1], 
                      [0, 1, 2]])
    return cv2.filter2D(frame, -1, kernel)

def apply_vignette(frame, level=0.8):
    height, width = frame.shape[:2]
    X = (cv2.getGaussianKernel(width, width/2) * level).T
    Y = cv2.getGaussianKernel(height, height/2) * level
    mask = Y * X
    mask = mask/mask.max()
    return (frame * np.dstack([mask]*3)).astype(np.uint8)

def apply_color_balance(frame, red=1.0, green=1.0, blue=1.0):
    frame = frame.astype(np.float32)
    frame[:,:,0] *= blue
    frame[:,:,1] *= green
    frame[:,:,2] *= red
    return np.clip(frame, 0, 255).astype(np.uint8)

def apply_pixelation(frame, pixel_size=8):
    h, w = frame.shape[:2]
    temp = cv2.resize(frame, (w//pixel_size, h//pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

def apply_cartoonization(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 9, 75, 75)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    color = cv2.bilateralFilter(frame, 9, 75, 75)
    return cv2.bitwise_and(color, color, mask=edges)

def apply_hdr_effect(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    lab = cv2.merge((l,a,b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# Filtre Uygulama Fonksiyonu
def apply_filter(filter_type, input_image, parameters=None):
    if input_image is None:
        return None
    
    frame = input_image.copy()
    
    # Temel Filtreler
    if filter_type == "Gaussian Blur":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif filter_type == "Sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        return cv2.filter2D(frame, -1, kernel)
    elif filter_type == "Edge Detection":
        return cv2.Canny(frame, 100, 200)
    elif filter_type == "Invert":
        return cv2.bitwise_not(frame)
    elif filter_type == "Grayscale":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Gelişmiş Filtreler
    elif filter_type == "Sepya Tonu":
        return apply_sepia(frame)
    elif filter_type == "Kabartma":
        return apply_emboss(frame)
    elif filter_type == "Vinyet":
        return apply_vignette(frame, parameters["vignette_level"])
    elif filter_type == "Renk Dengesi":
        return apply_color_balance(frame, parameters["red"], parameters["green"], parameters["blue"])
    elif filter_type == "Pikselleştirme":
        return apply_pixelation(frame, parameters["pixel_size"])
    elif filter_type == "Kartoon Efekti":
        return apply_cartoonization(frame)
    elif filter_type == "HDR Efekti":
        return apply_hdr_effect(frame)
    
    return frame

# Gradio Arayüzü
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📷 Profesyonel Görüntü Filtreleme Uygulaması")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Giriş Görüntüsü", type="numpy")
            
            with gr.Accordion("⚙️ Filtre Ayarları", open=True):
                filter_type = gr.Dropdown(
                    label="Filtre Seçin",
                    choices=[
                        "Gaussian Blur", "Sharpen", "Edge Detection",
                        "Invert", "Grayscale", "Sepya Tonu",
                        "Kabartma", "Vinyet", "Renk Dengesi",
                        "Pikselleştirme", "Kartoon Efekti", "HDR Efekti"
                    ],
                    value="Gaussian Blur"
                )
                
                with gr.Group(visible=False) as param_group:
                    vignette_level = gr.Slider(0.1, 1.0, value=0.7, label="Vinyet Şiddeti")
                    red_balance = gr.Slider(0.0, 2.0, value=1.0, label="Kırmızı Dengesi")
                    green_balance = gr.Slider(0.0, 2.0, value=1.0, label="Yeşil Dengesi")
                    blue_balance = gr.Slider(0.0, 2.0, value=1.0, label="Mavi Dengesi")
                    pixel_size = gr.Slider(2, 20, step=2, value=8, label="Piksel Boyutu")
            
            gr.Examples(
                examples=[
                    "sample_images/portrait.jpg",
                    "sample_images/landscape.jpg",
                    "sample_images/architecture.jpg"
                ],
                inputs=input_image,
                label="📁 Hızlı Örnekler"
            )
            
            apply_btn = gr.Button("Filtreyi Uygula", variant="primary")
        
        output_image = gr.Image(label="Filtrelenmiş Görüntü")

    # Parametre görünürlüğünü kontrol etme
    def toggle_parameters(selected_filter):
        advanced_filters = ["Vinyet", "Renk Dengesi", "Pikselleştirme"]
        return gr.Group(visible=selected_filter in advanced_filters)
    
    filter_type.change(
        fn=toggle_parameters,
        inputs=filter_type,
        outputs=param_group
    )

    # Filtre uygulama işlemi
    apply_btn.click(
        fn=apply_filter,
        inputs=[
            filter_type,
            input_image,
            gr.Dict({
                "vignette_level": vignette_level,
                "red": red_balance,
                "green": green_balance,
                "blue": blue_balance,
                "pixel_size": pixel_size
            })
        ],
        outputs=output_image
    )

demo.launch(share=True)