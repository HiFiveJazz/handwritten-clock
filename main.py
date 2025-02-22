import cairosvg
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

class SVGImageCycler(tk.Tk):
    def __init__(self, svg_folder1, svg_folder2, image_count=9, display_time=67):
        super().__init__()
        
        self.svg_folder1 = svg_folder1
        self.svg_folder2 = svg_folder2
        self.image_count = image_count
        self.display_time = display_time  # Time in milliseconds (1000ms = 1 second)
        self.current_image1 = 1  # Start from 1.svg
        self.current_image2 = 1  # Start from 1.svg for the second image
        
        # Set up the window
        self.title("SVG Image Cycler")
        
        # Update canvas size to fit both images side by side
        self.canvas = tk.Canvas(self, width=600, height=700)  # 300px width per image, 700px height for each
        self.canvas.pack()
        
        # Start cycling images
        self.cycle_images()
    
    def load_svg(self, svg_path):
        """Load an SVG file, convert it to PNG and return the image"""
        with open(svg_path, "rb") as svg_file:
            svg_data = svg_file.read()

        if not svg_data:
            raise ValueError("SVG file is empty")

        # Convert the SVG data to PNG data
        png_data = cairosvg.svg2png(bytestring=svg_data)
        image = Image.open(BytesIO(png_data))
        return image

    def display_images(self, image1, image2):
        """Display the two images on the Tkinter canvas side by side"""
        photo1 = ImageTk.PhotoImage(image1)
        photo2 = ImageTk.PhotoImage(image2)
        
        # Place the images on the canvas side by side
        self.canvas.create_image(150, 350, image=photo1)  # Position for the first image (centered on canvas)
        self.canvas.create_image(450, 350, image=photo2)  # Position for the second image (centered on canvas)
        
        # Keep references to the images
        self.canvas.image1 = photo1
        self.canvas.image2 = photo2
    
    def cycle_images(self):
        """Cycle through the SVG images and display them side by side"""
        # Construct the paths to the current SVG files
        svg_path1 = f"{self.svg_folder1}/{self.current_image1}.svg"
        svg_path2 = f"{self.svg_folder2}/{self.current_image2}.svg"
        
        try:
            # Load the two images
            image1 = self.load_svg(svg_path1)
            image2 = self.load_svg(svg_path2)
            
            # Display both images side by side
            self.display_images(image1, image2)
        except Exception as e:
            print(f"Error loading images: {e}")
        
        # Update the image indices and loop around
        self.current_image1 = self.current_image1 + 1 if self.current_image1 < self.image_count else 1
        self.current_image2 = self.current_image2 + 1 if self.current_image2 < self.image_count else 1
        
        # Schedule the next image update
        self.after(self.display_time, self.cycle_images)

if __name__ == "__main__":
    # Folder where the SVG files for each number are located
    svg_folder1 = "letters/1"
    svg_folder2 = "letters/2"
    
    # Create the SVGImageCycler instance and start the Tkinter main loop
    app = SVGImageCycler(svg_folder1, svg_folder2)
    app.mainloop()

