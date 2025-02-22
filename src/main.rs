use minifb::{Window, WindowOptions};
use resvg::usvg;
use tiny_skia::{Pixmap, Color};

fn main() {
    // Read the SVG file
    let svg_data = std::fs::read("letters/0/1.svg").expect("Failed to read SVG file");

    // Parse the SVG file using resvg
    let rtree = usvg::Tree::from_data(&svg_data, &usvg::Options::default())
        .expect("Failed to parse SVG file");

    // Get the dimensions of the SVG
    let width = rtree.svg_node().viewport.width() as u32;
    let height = rtree.svg_node().viewport.height() as u32;

    // Create a Pixmap to render the SVG
    let mut pixmap = Pixmap::new(width, height).expect("Failed to create Pixmap");

    // Render the SVG to the Pixmap
    let mut paint = tiny_skia::Paint::default();
    paint.set_color(Color::new(0, 0, 0, 255));  // Set the color to black

    rtree.render_to_pixmap(&mut pixmap, &paint).expect("Failed to render SVG to Pixmap");

    // Create a window to display the image
    let mut window = Window::new(
        "SVG Display",
        width as usize,
        height as usize,
        WindowOptions::default(),
    )
    .expect("Failed to create window");

    while window.is_open() {
        // Update the window with the rendered image
        window
            .update_with_buffer(pixmap.data(), width as usize, height as usize)
            .expect("Failed to update window");
    }
}

