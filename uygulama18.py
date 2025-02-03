import cv2 as cv
import numpy as np
import gradio as gr
import re

# Tuval boyutu
CANVAS_SIZE = (500, 500, 3)

# Boş bir tuval oluştur
def create_canvas():
    return np.ones(CANVAS_SIZE, dtype=np.uint8) * 255  # Beyaz arka plan

# Renk dönüşüm fonksiyonu: hex veya rgb formatlarını destekler
def hex_to_rgb(value):
    if value.startswith("#"):
        value = value.lstrip('#')
        return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
    elif value.startswith("rgb"):
        numbers = re.findall(r'\d+', value)
        if len(numbers) >= 3:
            return tuple(int(n) for n in numbers[:3])
    # Hata durumunda siyah döndür
    return (0, 0, 0)

# Şekil çizme fonksiyonu
def draw_shape(shape_type, radius_or_width, height, color, thickness, fill):
    canvas = create_canvas()
    # Tüm çizimler tuvalin ortasında yapılacak
    center = (CANVAS_SIZE[1] // 2, CANVAS_SIZE[0] // 2)
    
    # Eğer renk None ise varsayılan siyahı kullan
    if not color:
        color = "#000000"
    # Renk dönüşümü: RGB elde edip, ardından BGR'ye çeviriyoruz
    rgb_color = hex_to_rgb(color)
    bgr_color = tuple(reversed(rgb_color))
    
    if shape_type == "Circle":
        if fill:
            cv.circle(canvas, center, radius_or_width, bgr_color, cv.FILLED)
        else:
            cv.circle(canvas, center, radius_or_width, bgr_color, thickness)
    
    elif shape_type == "Rectangle":
        start = (center[0] - radius_or_width // 2, center[1] - height // 2)
        end = (center[0] + radius_or_width // 2, center[1] + height // 2)
        if fill:
            cv.rectangle(canvas, start, end, bgr_color, cv.FILLED)
        else:
            cv.rectangle(canvas, start, end, bgr_color, thickness)
    
    elif shape_type == "Ellipse":
        axes = (radius_or_width // 2, height // 2)
        if fill:
            cv.ellipse(canvas, center, axes, 0, 0, 360, bgr_color, cv.FILLED)
        else:
            cv.ellipse(canvas, center, axes, 0, 0, 360, bgr_color, thickness)
    
    elif shape_type == "Line":
        start = (center[0] - radius_or_width // 2, center[1] - height // 2)
        end = (center[0] + radius_or_width // 2, center[1] + height // 2)
        cv.line(canvas, start, end, bgr_color, thickness)
    
    return canvas

# Arayüz güncelleme fonksiyonu: seçilen şekle göre slider etiketlerini ayarlar
def update_inputs(shape):
    if shape == "Circle":
        return gr.update(label="Yarıçap"), gr.update(visible=False)
    elif shape == "Rectangle":
        return gr.update(label="Genişlik"), gr.update(label="Yükseklik", visible=True)
    elif shape == "Ellipse":
        return gr.update(label="Genişlik"), gr.update(label="Yükseklik", visible=True)
    elif shape == "Line":
        return gr.update(label="Uzunluk"), gr.update(label="Dikey Uzunluk", visible=True)

# Gradio arayüzü
with gr.Blocks() as demo:
    gr.Markdown("# OpenCV ile Geometrik Şekiller Çizme Uygulaması")
    
    with gr.Row():
        with gr.Column():
            shape_type = gr.Dropdown(["Circle", "Rectangle", "Ellipse", "Line"], label="Şekil Türü")
            with gr.Row():
                radius_or_width = gr.Slider(10, 250, value=100, step=1, label="Yarıçap")
                height = gr.Slider(10, 250, value=100, step=1, label="Yükseklik")
            color = gr.ColorPicker(label="Renk", value="#000000")
            thickness = gr.Slider(1, 20, value=2, step=1, label="Çizgi Kalınlığı")
            fill = gr.Checkbox(label="Dolu Şekil")
            draw_button = gr.Button("Şekli Çiz")
        with gr.Column():
            output_image = gr.Image(label="Çizilen Şekil")
    
    shape_type.change(fn=update_inputs, inputs=shape_type, outputs=[radius_or_width, height])
    
    draw_button.click(
        fn=draw_shape,
        inputs=[shape_type, radius_or_width, height, color, thickness, fill],
        outputs=output_image
    )

demo.launch()
