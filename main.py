import cv2
import numpy as np
from google.colab import files
from google.colab.patches import cv2_imshow
import ipywidgets as widgets
from IPython.display import display, clear_output

print("Step 1: Image upload karein")
uploaded = files.upload()

if uploaded:
    img_path = list(uploaded.keys())[0]
    original_img = cv2.imread(img_path)
    processed_img = original_img.copy()

    def show_everything():
        clear_output(wait=True)
        display(ui_layout)
        print(f"Current Filter: {filter_dropdown.value}")
        cv2_imshow(processed_img)

    def on_filter_change(change):
        global processed_img
        f = filter_dropdown.value
        img = original_img.copy()

        # --- 30 Options Logic ---
        if f == "Original": pass
        elif f == "Grayscale": img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif f == "Pencil Sketch (B&W)": _, img = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        elif f == "Pencil Sketch (Color)": img, _ = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        elif f == "Sepia":
            k = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
            img = cv2.transform(img, k)
        elif f == "Blur (Light)": img = cv2.GaussianBlur(img, (7, 7), 0)
        elif f == "Blur (Heavy)": img = cv2.GaussianBlur(img, (25, 25), 0)
        elif f == "Invert Colors": img = cv2.bitwise_not(img)
        elif f == "Sharpen":
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernel)
        elif f == "Emboss":
            kernel = np.array([[-2,-1,0], [-1,1,1], [0,1,2]])
            img = cv2.filter2D(img, -1, kernel)
        elif f == "Canny Edges": img = cv2.Canny(img, 100, 200)
        elif f == "Dilation":
            kernel = np.ones((5,5), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
        elif f == "Erosion":
            kernel = np.ones((5,5), np.uint8)
            img = cv2.erode(img, kernel, iterations=1)
        elif f == "Threshold":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        elif f == "Cartoon":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(img, 9, 300, 300)
            img = cv2.bitwise_and(color, color, mask=edges)
        elif f == "Rotate 90 CW": img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif f == "Rotate 90 CCW": img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif f == "Rotate 180": img = cv2.rotate(img, cv2.ROTATE_180)
        elif f == "Flip Horizontal": img = cv2.flip(img, 1)
        elif f == "Flip Vertical": img = cv2.flip(img, 0)
        elif f == "Brightness High": img = cv2.convertScaleAbs(img, alpha=1, beta=50)
        elif f == "Brightness Low": img = cv2.convertScaleAbs(img, alpha=1, beta=-50)
        elif f == "Contrast High": img = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
        elif f == "Summer": img = cv2.convertScaleAbs(img, alpha=1.2, beta=15)
        elif f == "Winter": img = cv2.convertScaleAbs(img, alpha=0.8, beta=10)
        elif f == "Stylization": img = cv2.stylization(img, sigma_s=60, sigma_r=0.07)
        elif f == "Bilateral Filter": img = cv2.bilateralFilter(img, 15, 75, 75)
        elif f == "Solarize":
            img = np.where(img < 128, img, 255 - img)
        elif f == "Gamma Correct":
            invGamma = 1.0 / 2.0
            table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            img = cv2.LUT(img, table)
        elif f == "Laplacian Edges":
            img = cv2.Laplacian(img, cv2.CV_64F).astype(np.uint8)

        processed_img = img
        show_everything()

    def apply_ai_enhance(b):
        global processed_img
        processed_img = cv2.detailEnhance(processed_img, sigma_s=10, sigma_r=0.15)
        show_everything()
        print("AI Smart Enhancement Applied!")

    def reset_btn_clk(b):
        global processed_img
        processed_img = original_img.copy()
        show_everything()

    def download_btn_clk(b):
        cv2.imwrite('final_edit.png', processed_img)
        files.download('final_edit.png')

    # --- UI Elements ---
    filter_options = [
        "Original", "Grayscale", "Pencil Sketch (B&W)", "Pencil Sketch (Color)",
        "Sepia", "Blur (Light)", "Blur (Heavy)", "Invert Colors", "Sharpen",
        "Emboss", "Canny Edges", "Laplacian Edges", "Dilation", "Erosion",
        "Threshold", "Cartoon", "Stylization", "Bilateral Filter", "Solarize",
        "Gamma Correct", "Rotate 90 CW", "Rotate 90 CCW", "Rotate 180",
        "Flip Horizontal", "Flip Vertical", "Brightness High", "Brightness Low",
        "Contrast High", "Summer", "Winter"
    ]

    filter_dropdown = widgets.Dropdown(options=filter_options, description='Filters:', layout={'width': 'max-content'})
    filter_dropdown.observe(on_filter_change, names='value')

    ai_enh_btn = widgets.Button(description="AI Smart Enhance", button_style='primary')
    reset_btn = widgets.Button(description="Reset All", button_style='danger')
    down_btn = widgets.Button(description="Download", button_style='success')

    ai_enh_btn.on_click(apply_ai_enhance)
    reset_btn.on_click(reset_btn_clk)
    down_btn.on_click(download_btn_clk)

    ui_layout = widgets.VBox([
        widgets.HBox([filter_dropdown, reset_btn]),
        widgets.HBox([widgets.Label("AI Boost:"), ai_enh_btn]),
        widgets.HBox([down_btn])
    ])

    show_everything()