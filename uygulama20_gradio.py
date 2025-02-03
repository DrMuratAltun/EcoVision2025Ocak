import cv2
import numpy as np
import gradio as gr

def draw_fractal(fractal_type, depth):
    canvas_size = 600
    canvas = np.ones((canvas_size, canvas_size, 3), dtype="uint8") * 255
    
    if fractal_type == "Sierpinski Triangle":
        points = [(300, 50), (50, 550), (550, 550)]
        draw_sierpinski(canvas, points, depth)
        
    elif fractal_type == "Koch Snowflake":
        start_points = [(150, 250), (450, 250), (300, 250 + 300)]
        for i in range(3):
            draw_koch(canvas, start_points[i], start_points[(i+1)%3], depth)
            
    elif fractal_type == "Barnsley Fern":
        draw_barnsley_fern(canvas, 100000)
        
    elif fractal_type == "Dragon Curve":
        draw_dragon_curve(canvas, depth)
    
    # OpenCV BGR -> RGB dönüşümü
    return cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

# Sierpinski Üçgeni Fonksiyonu
def draw_sierpinski(canvas, vertices, depth):
    if depth == 0:
        cv2.fillPoly(canvas, [np.array(vertices, dtype=np.int32)], (255,0,0))
    else:
        pt1 = ((vertices[0][0] + vertices[1][0])//2, (vertices[0][1] + vertices[1][1])//2)
        pt2 = ((vertices[1][0] + vertices[2][0])//2, (vertices[1][1] + vertices[2][1])//2)
        pt3 = ((vertices[2][0] + vertices[0][0])//2, (vertices[2][1] + vertices[0][1])//2)
        
        draw_sierpinski(canvas, [vertices[0], pt1, pt3], depth-1)
        draw_sierpinski(canvas, [pt1, vertices[1], pt2], depth-1)
        draw_sierpinski(canvas, [pt3, pt2, vertices[2]], depth-1)

# Koch Kar Tanesi Fonksiyonu (Düzeltildi)
def draw_koch(canvas, start, end, depth):
    if depth == 0:
        cv2.line(canvas, tuple(map(int, start)), tuple(map(int, end)), (0,0,255), 1)
    else:
        diff_x = end[0] - start[0]
        diff_y = end[1] - start[1]
        
        # Tüm noktalar integer'a dönüştürüldü
        p1 = (int(start[0] + diff_x/3), int(start[1] + diff_y/3))
        p3 = (int(start[0] + 2*diff_x/3), int(start[1] + 2*diff_y/3))
        
        angle = np.arctan2(diff_y, diff_x) - np.pi/3
        length = np.sqrt((diff_x/3)**2 + (diff_y/3)**2)
        p2 = (
            int(p1[0] + length*np.cos(angle)),
            int(p1[1] + length*np.sin(angle))
        )
        
        draw_koch(canvas, start, p1, depth-1)
        draw_koch(canvas, p1, p2, depth-1)
        draw_koch(canvas, p2, p3, depth-1)
        draw_koch(canvas, p3, end, depth-1)
# Barnsley Eğreltiotu Fonksiyonu
def draw_barnsley_fern(canvas, iterations):
    x, y = 0, 0
    for _ in range(iterations):
        r = np.random.random()
        if r < 0.01:
            x, y = 0, 0.16*y
        elif r < 0.86:
            x, y = 0.85*x + 0.04*y, -0.04*x + 0.85*y + 1.6
        elif r < 0.93:
            x, y = 0.2*x - 0.26*y, 0.23*x + 0.22*y + 1.6
        else:
            x, y = -0.15*x + 0.28*y, 0.26*x + 0.24*y + 0.44
        
        px = int(300 + x * 60)
        py = int(600 - y * 60)
        cv2.circle(canvas, (px, py), 1, (0,100,0), -1)

# Dragon Curve Fonksiyonu
def draw_dragon_curve(canvas, depth):
    def rotate(pivot, point, angle):
        s = np.sin(angle)
        c = np.cos(angle)
        x = point[0] - pivot[0]
        y = point[1] - pivot[1]
        return (int(x*c - y*s + pivot[0]), int(x*s + y*c + pivot[1]))
    
    points = [(200, 350), (400, 350)]
    for _ in range(depth):
        new_points = []
        for i in range(len(points)-1):
            mid = ((points[i][0]+points[i+1][0])//2, 
                  (points[i][1]+points[i+1][1])//2)
            rotated = rotate(points[i], mid, np.pi/2)
            new_points.extend([points[i], rotated])
        new_points.append(points[-1])
        points = new_points
    
    for i in range(len(points)-1):
        cv2.line(canvas, points[i], points[i+1], (255,0,255), 1)

# Gradio Arayüzü
with gr.Blocks() as demo:
    gr.Markdown("## 🌀 Fraktal Oluşturucu")
    with gr.Row():
        with gr.Column():
            fractal_type = gr.Dropdown(
                label="Fraktal Türü",
                choices=[
                    "Sierpinski Triangle",
                    "Koch Snowflake",
                    "Barnsley Fern",
                    "Dragon Curve"
                ],
                value="Sierpinski Triangle"
            )
            depth = gr.Slider(
                label="Detay Seviyesi",
                minimum=0,
                maximum=10,
                step=1,
                value=4
            )
        output_image = gr.Image(label="Fraktal Görünümü")

    fractal_type.change(draw_fractal, inputs=[fractal_type, depth], outputs=output_image)
    depth.change(draw_fractal, inputs=[fractal_type, depth], outputs=output_image)

demo.launch()