from PIL import Image, ImageOps
import numpy as np
import os

# Source path
src_path = "/Users/jorikschut/.gemini/antigravity/brain/edce318d-ef0c-4e17-90b4-6466e53cb62d/uploaded_image_1768581014999.png"
out_path = "/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-panorama.png"

try:
    img = Image.open(src_path).convert("RGB") # Start with RGB
    print(f"Original Dimensions: {img.size}")

    # 1. SMART COLOR & ALPHA CONVERSION
    # Instead of binary thresholding, we map darkness to opacity.
    # This preserves anti-aliasing (smooth edges) derived from the original image.
    
    # Invert image: White(255) -> 0 (Transparent), Black(0) -> 255 (Opaque)
    # Using the 'L' (Luminance) channel as the alpha map.
    grayscale = ImageOps.invert(img.convert("L"))
    
    # Create the target color block #0e4c92 (Sea Blue)
    sea_blue_rgb = (14, 76, 146)
    
    # Create a solid color image of the same size
    solid_color_img = Image.new("RGB", img.size, sea_blue_rgb)
    
    # Combine: Use the solid blue image, but apply the inverted grayscale as the Alpha channel
    img = solid_color_img.copy()
    img.putalpha(grayscale)
    
    # 2. Trim Whitespace (Crop to content based on new alpha)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f"Cropped to content: {bbox} -> {img.size}")
    
    # 3. Create Panoramic Canvas
    w, h = img.size
    
    # UPSCALING (Using 2.5x for crispness without over-blurring)
    # We rely on the natural anti-aliasing preserved above, so less extreme upscaling is needed
    target_scale = 2.5
    new_w = int(w * target_scale)
    new_h = int(h * target_scale)
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    w, h = img.size # Update w, h
    print(f"Upscaled tile size: {w}x{h} (Smooth Edges)")

    # 4. Create Panorama (Symmetric: Flip - Original - Flip)
    img_flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    img_arr = np.array(img)
    img_flipped_arr = np.array(img_flipped)
    
    combined_arr = np.hstack([img_flipped_arr, img_arr, img_flipped_arr])
    
    # 5. Save
    final_img = Image.fromarray(combined_arr)
    final_img.save(out_path)
    print(f"Saved smoothed panoramic skyline to {out_path}")

except Exception as e:
    print(f"Error: {e}")
