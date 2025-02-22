import cairosvg
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
import time

class SVGImageCycler(tk.Tk):
    def __init__(self, svg_folders, image_count=9, display_time=120, image_width=200):
        super().__init__()
        
        self.svg_folders = svg_folders
        self.image_count = image_count
        self.display_time = display_time  # Time in milliseconds (1000ms = 1 second)
        self.image_width = image_width  # Width for each image
        self.current_images = [1] * len(svg_folders)  # Start from 1.svg for each folder
        
        print("Caching Images ...")
        self.cached_images = {}  # Cache to store the images
        self.image_cache_ready = False  # Flag to indicate when images are ready

        # Set up the window
        self.title("SVG Image Cycler")
        # Calculate canvas width dynamically based on the number of folders (images)
        print("Calculating Dimension")
        canvas_width = self.image_width * len(svg_folders)  # Adjusted width per image
        self.canvas = tk.Canvas(self, width=canvas_width, height=700)  # 700px height for each image
        self.canvas.pack()
        print("Dimension Calculated")

        # Start caching images in a separate thread to avoid blocking the UI
        self.after(100, self.cache_images)  # Start caching process shortly after initialization

    def cache_images(self):
        """Cache all SVG images so they are ready for display"""
        images = []
        for i, svg_folder in enumerate(self.svg_folders):
            for img_num in range(1, self.image_count + 1):
                svg_path = f"{svg_folder}/{img_num}.svg"
                try:
                    # Load and cache the image
                    image = self.load_svg(svg_path)
                    self.cached_images[svg_path] = image
                except Exception as e:
                    print(f"Error caching image {svg_path}: {e}")
        
        self.image_cache_ready = True  # Set flag once caching is done
        print("Image caching complete. Starting image cycling.")
        
        # Start cycling images after the cache is ready
        self.cycle_images()

    def load_svg(self, svg_path):
        """Load an SVG file, convert it to PNG, resize, and return the image (caching it for later use)"""
        # Check if the image is cached
        if svg_path in self.cached_images:
            return self.cached_images[svg_path]
        
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
        image = image.resize((self.image_width, new_height), Image.Resampling.LANCZOS)

        # Cache the image
        self.cached_images[svg_path] = image
        
        return image

    def display_images(self, images):
        """Display the images on the Tkinter canvas side by side"""
        photo_images = [ImageTk.PhotoImage(img) for img in images]
        
        # Clear the canvas to only show updated images
        self.canvas.delete("all")
        
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
        if not self.image_cache_ready:
            # If images are not ready, just keep waiting
            self.after(100, self.cycle_images)
            return
        
        # Get the current time in 12-hour format with AM/PM
        current_time = time.strftime('%I:%M %p')  # Format as "12:34 AM"
        
        # Split the current time into its characters (e.g., "1", "2", ":", "3", "4", " ", "A", "M")
        time_chars = list(current_time)
        
        images = []
        
        # Map each character of the time string to the corresponding SVG image
        for i, char in enumerate(time_chars):
            # Calculate the current image index for each character
            folder_name = ""
            if char == ' ':
                folder_name = "letters/Space"
            elif char == ':':
                folder_name = "letters/:"
            elif char == 'A' or char == 'P':
                folder_name = f"letters/{char}"
            else:
                folder_name = f"letters/{char}"
            
            # Cycle through the images in each folder (1 to 9)
            current_image = (self.current_images[i] % self.image_count) + 1  # Loop through 1 to 9
            svg_path = f"{folder_name}/{current_image}.svg"
            
            try:
                # Load and append the image
                image = self.cached_images[svg_path]
                images.append(image)
            except KeyError:
                print(f"Error: Image not found for {svg_path}")
                # If not found, you can reload it
                images.append(self.load_svg(svg_path))

            # Update the image index for the next cycle
            self.current_images[i] = (self.current_images[i] + 1) if self.current_images[i] < self.image_count else 1

        # Display the images for the current time
        self.display_images(images)
        
        # Schedule the next image update after the specified display time
        self.after(self.display_time, self.cycle_images)

if __name__ == "__main__":
    # Folders where the SVG files for each number and special character are located
    svg_folders = [
        "letters/1", "letters/2", "letters/3", "letters/4", "letters/5", 
        "letters/6", "letters/7", "letters/8", "letters/9", "letters/0",
        "letters/Space", "letters/:", "letters/A", "letters/P"
    ]  # Add as many folders as needed
    
    # Create the SVGImageCycler instance and start the Tkinter main loop
    app = SVGImageCycler(svg_folders)
    app.mainloop()

