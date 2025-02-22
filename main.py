import cairosvg
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

class SVGImageCycler(tk.Tk):
    def __init__(self, svg_folders, image_count=9, display_time=67, image_width=200):
        super().__init__()
        
        self.svg_folders = svg_folders
        self.image_count = image_count
        self.display_time = display_time  # Time in milliseconds (1000ms = 1 second)
        self.image_width = image_width  # Width for each image
        self.current_images = [1] * len(svg_folders)  # Start from 1.svg for each folder
        
        # Set up the window
        self.title("SVG Image Cycler")
        
        # Calculate canvas width dynamically based on the number of folders (images)
        canvas_width = self.image_width * len(svg_folders)  # Adjusted width per image
        self.canvas = tk.Canvas(self, width=canvas_width, height=700)  # 700px height for each image
        self.canvas.pack()
        
        # Start cycling images
        self.cycle_images()
    
    def load_svg(self, svg_path):
        """Load an SVG file, convert it to PNG, resize, and return the image"""
        with open(svg_path, "rb") as svg_file:
            svg_data = svg_file.read()

        if not svg_data:
            raise ValueError("SVG file is empty")

        # Convert the SVG data to PNG data
        png_data = cairosvg.svg2png(bytestring=svg_data)
        image = Image.open(BytesIO(png_data))

        # Scale down the image to fit within the desired width
        width_percent = (self.image_width / float(image.width))
        new_height = int((float(image.height) * float(width_percent)))
        image = image.resize((self.image_width, new_height), Image.Resampling.LANCZOS)  # Updated resampling method
        
        return image

    def display_images(self, images):
        """Display the images on the Tkinter canvas side by side"""
        photo_images = [ImageTk.PhotoImage(img) for img in images]
        
        # Place the images on the canvas side by side
        x_offset = self.image_width // 2  # Initial X position, centered for each image
        for i, photo in enumerate(photo_images):
            self.canvas.create_image(x_offset, 350, image=photo)  # Position images horizontally
            x_offset += self.image_width  # Move image_width pixels to the right for the next image
        
        # Keep references to the images to avoid them being garbage collected
        for i, photo in enumerate(photo_images):
            setattr(self.canvas, f"image{i}", photo)
    
    def cycle_images(self):
        """Cycle through the SVG images and display them side by side"""
        images = []
        
        for i, svg_folder in enumerate(self.svg_folders):
            svg_path = f"{svg_folder}/{self.current_images[i]}.svg"
            try:
                # Load the image
                image = self.load_svg(svg_path)
                images.append(image)
            except Exception as e:
                print(f"Error loading image {svg_path}: {e}")
        
        # Display the images side by side
        self.display_images(images)
        
        # Update the image indices and loop around
        self.current_images = [
            (img + 1) if img < self.image_count else 1
            for img in self.current_images
        ]
        
        # Schedule the next image update
        self.after(self.display_time, self.cycle_images)

if __name__ == "__main__":
    # Folders where the SVG files for each number are located
    svg_folders = ["letters/1", "letters/2", "letters/:", "letters/3", "letters/4"]  # Add as many folders as needed
    
    # Create the SVGImageCycler instance and start the Tkinter main loop
    app = SVGImageCycler(svg_folders)
    app.mainloop()

