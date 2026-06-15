"""
AURA // On-Device Image Captioning AI
------------------------------------
This is a simple, lightweight Python GUI application that loads a pre-trained
multimodal model (Salesforce BLIP-Base) to generate text captions for images.

Everything runs locally on your computer.

Dependencies:
    pip install customtkinter transformers torch pillow
"""

import os
import threading
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog

# -----------------------------------------------------------------------------
# 1. AI Model Loader & Captioner (Using PyTorch and Hugging Face Transformers)
# -----------------------------------------------------------------------------

# We import the required Hugging Face classes.
# - BlipProcessor: Prepares the image (resizing, normalizing) and decodes text tokens.
# - BlipForConditionalGeneration: The neural network combining vision and text generation.
from transformers import BlipProcessor, BlipForConditionalGeneration

# Global variables to store the loaded model and processor so we only load them once.
processor = None
model = None

# Detect if your laptop has a CUDA-compatible GPU. If not, default to the CPU.
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model_and_processor():
    """Downloads (first run only) and loads the BLIP model into memory."""
    global processor, model
    
    if model is None:
        # Load the pre-trained processor (handles image resizing and text decoding) locally
        processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base",
            local_files_only=True
        )
        
        # Load the pre-trained neural network weights (force using the cached pytorch_model.bin locally)
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base", 
            use_safetensors=False, 
            local_files_only=True
        )
        
        # Move the model to the target device (CPU or GPU)
        model.to(device)

def run_captioning_inference(image_path):
    """Loads an image, runs it through the neural network, and returns a caption string."""
    # Ensure the model is loaded in memory before running captioning
    load_model_and_processor()
    
    # Open the image file using the Python Imaging Library (PIL) and convert it to RGB
    raw_image = Image.open(image_path).convert('RGB')
    
    # Preprocess the image and convert it to PyTorch tensors (multi-dimensional math arrays)
    inputs = processor(raw_image, return_tensors="pt")
    
    # Move the inputs to CPU or GPU to match the model location
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Run the model to generate the caption (max_new_tokens limits the sentence length)
    out = model.generate(**inputs, max_new_tokens=40)
    
    # Decode the mathematical output tokens back into a readable English string
    caption = processor.decode(out[0], skip_special_tokens=True)
    
    # Return the clean text caption
    return caption


# -----------------------------------------------------------------------------
# 2. GUI Application Class (Using CustomTkinter)
# -----------------------------------------------------------------------------

class ImageCaptionerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Define window title and dimensions
        self.title("AURA // Image Captioning AI")
        self.geometry("620x680")
        self.resizable(False, False)

        # Set clean minimalistic white and grey theme
        # "light" gives us a clean white/light-grey background
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue") # Standard CTK button theme
        
        # Track the path of the loaded image
        self.current_image_path = None
        
        # Build the user interface layout
        self.setup_ui()

    def setup_ui(self):
        """Creates and places all visual elements in the window."""
        
        # --- TITLE SECTION ---
        title_label = ctk.CTkLabel(
            self, 
            text="AURA // VISION AI", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#1a1a1a"
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = ctk.CTkLabel(
            self, 
            text="On-Device Image to Text Captioning", 
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="#808080"
        )
        subtitle_label.pack(pady=(0, 20))

        # --- IMAGE DISPLAY FRAME ---
        # A grey bordered container where the selected image will be previewed.
        self.image_frame = ctk.CTkFrame(
            self, 
            width=500, 
            height=300, 
            fg_color="#f2f2f5", 
            border_color="#d1d1d6", 
            border_width=1
        )
        self.image_frame.pack_propagate(False) # Prevent frame from shrinking to label size
        self.image_frame.pack(pady=10)

        # Placeholder label inside the frame
        self.image_label = ctk.CTkLabel(
            self.image_frame, 
            text="No image selected.\nClick 'Browse Image' or select a sample below.",
            text_color="#8e8e93",
            font=ctk.CTkFont(family="Helvetica", size=13)
        )
        self.image_label.pack(expand=True, fill="both")

        # --- CONTROLS FRAME ---
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.pack(pady=15, fill="x", padx=60) # Padding on X

        # Browse Image Button: opens Windows File Explorer directly
        self.browse_btn = ctk.CTkButton(
            controls_frame, 
            text="📁 Browse Image...", 
            command=self.open_file_dialog,
            fg_color="#e5e5ea",
            text_color="#1c1c1e",
            hover_color="#d1d1d6",
            font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
            width=180
        )
        self.browse_btn.pack(side="left", padx=(60, 10))

        # Samples Frame (handles loading pre-existing sample images)
        samples_label = ctk.CTkLabel(controls_frame, text="Samples:", text_color="#8e8e93", font=ctk.CTkFont(size=11))
        samples_label.pack(side="left", padx=5)

        for i in range(1, 4):
            btn = ctk.CTkButton(
                controls_frame, 
                text=str(i), 
                width=30,
                height=30,
                fg_color="#f2f2f5",
                text_color="#1c1c1e",
                hover_color="#e5e5ea",
                border_color="#d1d1d6",
                border_width=1,
                command=lambda num=i: self.load_sample(num)
            )
            btn.pack(side="left", padx=3)

        # --- GENERATION SECTION ---
        # The main action button to trigger the caption logic
        self.generate_btn = ctk.CTkButton(
            self, 
            text="⚡ Generate Caption", 
            command=self.trigger_generation,
            fg_color="#2c2c2e",
            text_color="#ffffff",
            hover_color="#1c1c1e",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            height=45,
            width=500,
            state="disabled" # Disabled until an image is loaded
        )
        self.generate_btn.pack(pady=10)

        # --- CAPTION OUTPUT BOX ---
        # A clean, light-grey display area showing the generated caption
        self.output_frame = ctk.CTkFrame(
            self, 
            width=500, 
            height=80, 
            fg_color="#f8f8fa", 
            border_color="#e5e5ea", 
            border_width=1
        )
        self.output_frame.pack_propagate(False)
        self.output_frame.pack(pady=10)

        self.caption_display = ctk.CTkLabel(
            self.output_frame, 
            text="", 
            font=ctk.CTkFont(family="Helvetica", size=14, slant="italic"),
            text_color="#1c1c1e",
            wraplength=460
        )
        self.caption_display.pack(expand=True, fill="both", padx=20)

        # --- STATUS BAR ---
        # Bottom status log indicating model state and run location
        self.status_bar = ctk.CTkLabel(
            self, 
            text=f"Status: Ready  |  Device: {device.upper()}", 
            font=ctk.CTkFont(family="Helvetica", size=11),
            text_color="#8e8e93"
        )
        self.status_bar.pack(side="bottom", pady=15)

    # -------------------------------------------------------------
    # 3. GUI Interaction Logic
    # -------------------------------------------------------------

    def open_file_dialog(self):
        """Opens the native Windows File Explorer to select an image."""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if file_path:
            self.display_image(file_path)

    def load_sample(self, num):
        """Loads one of the pre-generated sample files from the directory."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_path = os.path.join(script_dir, f"sample{num}.png")
        
        if os.path.exists(sample_path):
            self.display_image(sample_path)
        else:
            self.update_status(f"Error: sample{num}.png not found in directory.")

    def display_image(self, path):
        """Resizes the image and renders it inside the GUI frame."""
        self.current_image_path = path
        
        try:
            # Open the image file using PIL
            pil_image = Image.open(path)
            
            # Calculate aspect ratio to fit the image inside our 500x300 container
            max_width, max_height = 500, 300
            width, height = pil_image.size
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            # Resize the image
            resized_pil = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert PIL image to CustomTkinter image
            self.ctk_image = ctk.CTkImage(
                light_image=resized_pil, 
                dark_image=resized_pil, 
                size=(new_width, new_height)
            )
            
            # Configure label to display the image
            self.image_label.configure(image=self.ctk_image, text="")
            self.image_label.image = self.ctk_image  # Keep reference
            
            # Enable the Generate button
            self.generate_btn.configure(state="normal")
            self.caption_display.configure(text="")
            self.update_status("Image loaded. Click 'Generate Caption' to begin.")
            
        except Exception as e:
            self.update_status(f"Error loading image: {str(e)}")

    def trigger_generation(self):
        """Runs the captioning model on a background thread to prevent UI freezing."""
        if not self.current_image_path:
            return

        # Update button and status to indicate loading/inference state
        self.generate_btn.configure(state="disabled", text="⚡ Processing...")
        self.update_status("Processing... (Downloading model weights on first run)")
        self.caption_display.configure(text="Decoding features...")

        # Inner helper run function for the thread
        def run():
            try:
                # Execute the heavy ML pipeline
                caption = run_captioning_inference(self.current_image_path)
                
                # Safely return to the main thread to update the UI
                self.after(0, lambda: self.show_success(caption))
            except Exception as e:
                # Capture the error message as a standard local variable
                error_message = str(e)
                # Safely return to the main thread to show the error
                self.after(0, lambda: self.show_error(error_message))

        # Launch the threading background task
        # daemon=True ensures the thread terminates automatically if the window is closed
        threading.Thread(target=run, daemon=True).start()

    def show_success(self, caption):
        """Callback showing the generated caption."""
        self.caption_display.configure(text=caption)
        self.generate_btn.configure(state="normal", text="⚡ Generate Caption")
        self.update_status("Caption generated successfully.")

    def show_error(self, error_message):
        """Callback showing error details."""
        self.caption_display.configure(text=f"Error: {error_message}")
        self.generate_btn.configure(state="normal", text="⚡ Generate Caption")
        self.update_status("Error occurred during captioning.")

    def update_status(self, text):
        """Updates the status bar text."""
        self.status_bar.configure(text=f"Status: {text}  |  Device: {device.upper()}")


# -----------------------------------------------------------------------------
# 4. Program Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Create the application instance
    app = ImageCaptionerApp()
    
    # Run the Tkinter main event loop (keeps the window open and listening for events)
    app.mainloop()
