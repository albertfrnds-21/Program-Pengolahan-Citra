import customtkinter as ctk
from tkinter import filedialog, Canvas
from PIL import Image, ImageTk
import numpy as np
import cv2

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageEnhancementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Enhancement System")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        
        self.original_image = None
        self.processed_image = None
        self.current_image = None  # For real-time adjustments
        
        # Parameters for sliders
        self.brightness_value = 0
        self.contrast_value = 1.0
        self.gamma_value = 1.0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, width=220, corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=(0, 5))
        self.sidebar.pack_propagate(False)
        
        # Content area
        self.content_area = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.content_area.pack(side="left", fill="both", expand=True)
        
        self.setup_sidebar()
        self.setup_content_area()
    
    def setup_sidebar(self):
        # Title
        title = ctk.CTkLabel(self.sidebar, text="Enhancement", 
                            font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10, padx=10)
        
        # File Operations
        file_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        file_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(file_frame, text="📁 Load", 
                     command=self.load_image, height=32, font=ctk.CTkFont(size=12)).pack(fill="x", pady=2)
        ctk.CTkButton(file_frame, text="💾 Save", 
                     command=self.save_image, height=32, font=ctk.CTkFont(size=12)).pack(fill="x", pady=2)
        ctk.CTkButton(file_frame, text="🔄 Reset", 
                     command=self.reset_image, height=32, font=ctk.CTkFont(size=12)).pack(fill="x", pady=2)
        
        # Separator
        ctk.CTkLabel(self.sidebar, text="─" * 25, font=ctk.CTkFont(size=10)).pack(pady=5)
        
        # Histogram Operations
        hist_label = ctk.CTkLabel(self.sidebar, text="Histogram", 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        hist_label.pack(pady=5)
        
        hist_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        hist_frame.pack(pady=2, padx=10, fill="x")
        
        ctk.CTkButton(hist_frame, text="Equalization", 
                     command=self.histogram_equalization, height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(hist_frame, text="Spec (Gray)", 
                     command=lambda: self.histogram_specification("gray"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(hist_frame, text="Spec (HSV)", 
                     command=lambda: self.histogram_specification("hsv"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(hist_frame, text="Spec (LAB)", 
                     command=lambda: self.histogram_specification("lab"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(hist_frame, text="CLAHE", 
                     command=self.apply_clahe, height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        
        # Separator
        ctk.CTkLabel(self.sidebar, text="─" * 25, font=ctk.CTkFont(size=10)).pack(pady=5)
        
        # Convolution Operations
        conv_label = ctk.CTkLabel(self.sidebar, text="Convolution", 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        conv_label.pack(pady=5)
        
        conv_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        conv_frame.pack(pady=2, padx=10, fill="x")
        
        ctk.CTkButton(conv_frame, text="Smoothing", 
                     command=lambda: self.apply_convolution("smoothing"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(conv_frame, text="Gaussian", 
                     command=lambda: self.apply_convolution("gaussian"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(conv_frame, text="Sharpening", 
                     command=lambda: self.apply_convolution("sharpening"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(conv_frame, text="Sobel Edge", 
                     command=lambda: self.apply_convolution("sobel"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)
        ctk.CTkButton(conv_frame, text="Laplacian", 
                     command=lambda: self.apply_convolution("laplacian"), height=28, font=ctk.CTkFont(size=11)).pack(fill="x", pady=2)

    
    def setup_content_area(self):
        # Top controls (sliders)
        controls_frame = ctk.CTkFrame(self.content_area, height=130, corner_radius=10)
        controls_frame.pack(fill="x", padx=5, pady=5)
        controls_frame.pack_propagate(False)
        
        # Brightness slider
        brightness_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        brightness_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(brightness_frame, text="Brightness:", 
                    font=ctk.CTkFont(size=12, weight="bold"), width=80).pack(side="left", padx=5)
        self.brightness_label = ctk.CTkLabel(brightness_frame, text="0", width=40)
        self.brightness_label.pack(side="right", padx=5)
        self.brightness_slider = ctk.CTkSlider(brightness_frame, from_=-100, to=100, 
                                              command=self.on_brightness_change, width=300)
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side="right", padx=5, fill="x", expand=True)
        
        # Contrast slider
        contrast_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        contrast_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(contrast_frame, text="Contrast:", 
                    font=ctk.CTkFont(size=12, weight="bold"), width=80).pack(side="left", padx=5)
        self.contrast_label = ctk.CTkLabel(contrast_frame, text="1.0", width=40)
        self.contrast_label.pack(side="right", padx=5)
        self.contrast_slider = ctk.CTkSlider(contrast_frame, from_=0.5, to=3.0, 
                                            command=self.on_contrast_change, width=300)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(side="right", padx=5, fill="x", expand=True)
        
        # Gamma slider
        gamma_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        gamma_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(gamma_frame, text="Gamma:", 
                    font=ctk.CTkFont(size=12, weight="bold"), width=80).pack(side="left", padx=5)
        self.gamma_label = ctk.CTkLabel(gamma_frame, text="1.0", width=40)
        self.gamma_label.pack(side="right", padx=5)
        self.gamma_slider = ctk.CTkSlider(gamma_frame, from_=0.1, to=3.0, 
                                         command=self.on_gamma_change, width=300)
        self.gamma_slider.set(1.0)
        self.gamma_slider.pack(side="right", padx=5, fill="x", expand=True)
        
        # Images and histograms container
        display_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        display_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Left side - Original
        left_frame = ctk.CTkFrame(display_frame, corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        
        ctk.CTkLabel(left_frame, text="Original", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.original_canvas = Canvas(left_frame, width=480, height=450, bg="#2b2b2b", highlightthickness=0)
        self.original_canvas.pack(pady=5)
        
        # Right side - Processed
        right_frame = ctk.CTkFrame(display_frame, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=3, pady=3)
        
        ctk.CTkLabel(right_frame, text="Processed", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.processed_canvas = Canvas(right_frame, width=480, height=450, bg="#2b2b2b", highlightthickness=0)
        self.processed_canvas.pack(pady=5)
        
        # Status bar
        self.status_label = ctk.CTkLabel(self.content_area, text="Ready. Load an image to start.", 
                                        font=ctk.CTkFont(size=11))
        self.status_label.pack(pady=3)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All files", "*.*")]
        )
        
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.current_image = self.original_image.copy()
            self.processed_image = None
            
            self.display_image(self.original_image, self.original_canvas)
            
            # Clear processed side
            self.processed_canvas.delete("all")
            
            # Reset sliders
            self.brightness_slider.set(0)
            self.contrast_slider.set(1.0)
            self.gamma_slider.set(1.0)
            
            self.status_label.configure(text=f"Image loaded: {file_path.split('/')[-1]}")
    
    def display_image(self, image, canvas):
        if image is None:
            return
        
        h, w = image.shape[:2]
        canvas_width = canvas.winfo_reqwidth()
        canvas_height = canvas.winfo_reqheight()
        
        scale = min(canvas_width/w, canvas_height/h)
        new_w, new_h = int(w*scale), int(h*scale)
        
        resized = cv2.resize(image, (new_w, new_h))
        img_pil = Image.fromarray(resized)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, image=img_tk)
        canvas.image = img_tk
    
    def display_histogram(self, image, canvas):
        if image is None:
            return
        
        canvas.delete("all")
        
        # Calculate histograms
        colors = ['red', 'green', 'blue']
        hist_height = 85
        hist_width = 360
        margin = 10
        
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            hist = hist.flatten()
            
            # Normalize
            if hist.max() > 0:
                hist = hist / hist.max() * hist_height
            
            # Draw histogram with thicker lines
            for j in range(256):
                x = margin + (j * hist_width / 256)
                y_start = margin + hist_height
                y_end = margin + hist_height - hist[j]
                canvas.create_line(x, y_start, x, y_end, fill=color, width=2)
        
        # Draw border and labels
        canvas.create_rectangle(margin, margin, margin + hist_width, margin + hist_height, 
                              outline="gray", width=1)
        canvas.create_text(margin + hist_width // 2, margin + hist_height + 10, 
                         text="RGB Histogram", fill="white", font=("Arial", 9))

    
    def on_brightness_change(self, value):
        if self.original_image is None:
            return
        
        self.brightness_value = int(value)
        self.brightness_label.configure(text=f"{self.brightness_value}")
        self.apply_realtime_adjustments()
    
    def on_contrast_change(self, value):
        if self.original_image is None:
            return
        
        self.contrast_value = float(value)
        self.contrast_label.configure(text=f"{self.contrast_value:.2f}")
        self.apply_realtime_adjustments()
    
    def on_gamma_change(self, value):
        if self.original_image is None:
            return
        
        self.gamma_value = float(value)
        self.gamma_label.configure(text=f"{self.gamma_value:.2f}")
        self.apply_realtime_adjustments()
    
    def apply_realtime_adjustments(self):
        if self.original_image is None:
            return
        
        # Start with original or current processed image
        if self.processed_image is not None:
            base_image = self.processed_image.copy()
        else:
            base_image = self.original_image.copy()
        
        # Apply brightness
        adjusted = base_image.astype(np.float32)
        adjusted = adjusted + self.brightness_value
        
        # Apply contrast
        adjusted = adjusted * self.contrast_value
        
        # Apply gamma correction
        if self.gamma_value != 1.0:
            inv_gamma = 1.0 / self.gamma_value
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
            adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
            adjusted = cv2.LUT(adjusted, table)
        else:
            adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        
        self.current_image = adjusted
        self.display_image(adjusted, self.processed_canvas)
    
    def reset_image(self):
        if self.original_image is None:
            return
        
        self.processed_image = None
        self.current_image = self.original_image.copy()
        
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        
        self.processed_canvas.delete("all")
        
        self.status_label.configure(text="Image reset to original")
    
    def histogram_equalization(self):
        if self.original_image is None:
            self.status_label.configure(text="Please load an image first!")
            return
        
        # Convert to YCrCb and equalize Y channel
        ycrcb = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
        
        self.processed_image = result
        self.current_image = result.copy()
        
        # Reset sliders
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        
        self.display_image(result, self.processed_canvas)
        self.status_label.configure(text="Histogram Equalization applied")
    
    def histogram_specification(self, mode):
        if self.original_image is None:
            self.status_label.configure(text="Please load an image first!")
            return
        
        if mode == "gray":
            # Grayscale histogram specification
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            
            # Target histogram (uniform distribution)
            target_hist = np.ones(256) * (gray.size / 256)
            
            # Calculate CDF
            hist_original = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
            cdf_original = hist_original.cumsum()
            cdf_original = cdf_original / cdf_original[-1]
            
            cdf_target = target_hist.cumsum()
            cdf_target = cdf_target / cdf_target[-1]
            
            # Mapping
            mapping = np.zeros(256, dtype=np.uint8)
            for i in range(256):
                diff = np.abs(cdf_target - cdf_original[i])
                mapping[i] = np.argmin(diff)
            
            result = mapping[gray]
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
            
        elif mode == "hsv":
            # HSV color histogram specification
            hsv = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV)
            v_channel = hsv[:, :, 2]
            
            # Apply histogram specification to V channel
            target_hist = np.ones(256) * (v_channel.size / 256)
            hist_original = cv2.calcHist([v_channel], [0], None, [256], [0, 256]).flatten()
            cdf_original = hist_original.cumsum()
            cdf_original = cdf_original / cdf_original[-1]
            
            cdf_target = target_hist.cumsum()
            cdf_target = cdf_target / cdf_target[-1]
            
            mapping = np.zeros(256, dtype=np.uint8)
            for i in range(256):
                diff = np.abs(cdf_target - cdf_original[i])
                mapping[i] = np.argmin(diff)
            
            hsv[:, :, 2] = mapping[v_channel]
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            
        elif mode == "lab":
            # LAB color histogram specification
            lab = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2LAB)
            l_channel = lab[:, :, 0]
            
            # Apply histogram specification to L channel
            target_hist = np.ones(256) * (l_channel.size / 256)
            hist_original = cv2.calcHist([l_channel], [0], None, [256], [0, 256]).flatten()
            cdf_original = hist_original.cumsum()
            cdf_original = cdf_original / cdf_original[-1]
            
            cdf_target = target_hist.cumsum()
            cdf_target = cdf_target / cdf_target[-1]
            
            mapping = np.zeros(256, dtype=np.uint8)
            for i in range(256):
                diff = np.abs(cdf_target - cdf_original[i])
                mapping[i] = np.argmin(diff)
            
            lab[:, :, 0] = mapping[l_channel]
            result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        self.processed_image = result
        self.current_image = result.copy()
        
        # Reset sliders
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        
        self.display_image(result, self.processed_canvas)
        self.status_label.configure(text=f"Histogram Specification ({mode.upper()}) applied")

    
    def apply_clahe(self):
        if self.original_image is None:
            self.status_label.configure(text="Please load an image first!")
            return
        
        # Convert to LAB and apply CLAHE to L channel
        lab = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        self.processed_image = result
        self.current_image = result.copy()
        
        # Reset sliders
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        
        self.display_image(result, self.processed_canvas)
        self.status_label.configure(text="CLAHE (Adaptive Histogram) applied")
    
    def apply_convolution(self, mask_type):
        if self.original_image is None:
            self.status_label.configure(text="Please load an image first!")
            return
        
        kernels = {
            "smoothing": np.ones((5, 5), np.float32) / 25,
            "gaussian": cv2.getGaussianKernel(5, 1.0) @ cv2.getGaussianKernel(5, 1.0).T,
            "sharpening": np.array([[-1, -1, -1],
                                   [-1,  9, -1],
                                   [-1, -1, -1]]),
            "laplacian": np.array([[0, -1, 0],
                                  [-1, 4, -1],
                                  [0, -1, 0]])
        }
        
        if mask_type == "sobel":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel = np.sqrt(sobel_x**2 + sobel_y**2)
            sobel = np.uint8(np.clip(sobel, 0, 255))
            result = cv2.cvtColor(sobel, cv2.COLOR_GRAY2RGB)
        else:
            kernel = kernels[mask_type]
            result = cv2.filter2D(self.original_image, -1, kernel)
            result = np.clip(result, 0, 255).astype(np.uint8)
        
        self.processed_image = result
        self.current_image = result.copy()
        
        # Reset sliders
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        
        self.display_image(result, self.processed_canvas)
        self.status_label.configure(text=f"Convolution ({mask_type}) applied")
    
    def auto_enhance(self):
        if self.original_image is None:
            self.status_label.configure(text="Please load an image first!")
            return
        
        # Step 1: CLAHE for contrast enhancement
        lab = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        # Step 2: Denoise
        result = cv2.fastNlMeansDenoisingColored(result, None, 10, 10, 7, 21)
        
        # Step 3: Light sharpening
        kernel = np.array([[-0.5, -0.5, -0.5],
                          [-0.5,  5.0, -0.5],
                          [-0.5, -0.5, -0.5]])
        result = cv2.filter2D(result, -1, kernel)
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        self.processed_image = result
        self.current_image = result.copy()
        
        # Reset sliders
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.gamma_slider.set(1.0)
        
        self.display_image(result, self.processed_canvas)
        self.status_label.configure(text="Auto Enhance applied (CLAHE + Denoise + Sharpening)")
    
    def save_image(self):
        if self.current_image is None:
            self.status_label.configure(text="No processed image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            image_to_save = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, image_to_save)
            self.status_label.configure(text=f"Image saved: {file_path.split('/')[-1]}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageEnhancementApp(root)
    root.mainloop()
