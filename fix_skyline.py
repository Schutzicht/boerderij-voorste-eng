from PIL import Image, ImageOps
import numpy as np
import os

# Source path
src_path = "/Users/jorikschut/.gemini/antigravity/brain/edce318d-ef0c-4e17-90b4-6466e53cb62d/uploaded_image_1768581660488.png"
out_path = "/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-panorama.png"

try:
    img = Image.open(src_path).convert("RGBA")
    print(f"Original Dimensions: {img.size}")

    # 1. REMOVE BACKGROUND & COLORIZE
    # User: "zonder achtergrond" and "maak de skyline blauw"
    
    data = np.array(img)
    # data shape is (Height, Width, 4)
    
    # Create target array (Initialized as transparent)
    new_data = np.zeros_like(data)
    
    # Target Blue
    target_blue = [14, 76, 146] 
    
    threshold = 240 # Tolerance for "white"
    
    # Access channels directly
    r = data[:, :, 0]
    g = data[:, :, 1]
    b = data[:, :, 2]
    a = data[:, :, 3]
    
    # Mask: Content IS pixels where (Red < 240 OR Green < 240 OR Blue < 240) AND Alpha > 0
    is_not_white = (r < threshold) | (g < threshold) | (b < threshold)
    has_alpha = (a > 20)
    
    content_mask = is_not_white & has_alpha
    
    # Apply Blue Color to Content
    new_data[content_mask, 0] = target_blue[0]
    new_data[content_mask, 1] = target_blue[1]
    new_data[content_mask, 2] = target_blue[2]
    new_data[content_mask, 3] = 255 # Make content fully opaque
    
    img = Image.fromarray(new_data)
    
    # 2. Trim whitespace
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f"Cropped to content: {bbox} -> {img.size}")
    
    # 3. Upscale (High Quality)
    w, h = img.size
    target_scale = 3.0 
    new_w = int(w * target_scale)
    new_h = int(h * target_scale)
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    print(f"Upscaled tile size: {img.size}")

    # 4. Create Panorama (Simple Repetition)
    img_arr = np.array(img)
    combined_arr = np.hstack([img_arr, img_arr, img_arr])
    
    # 5. Save
    final_img = Image.fromarray(combined_arr)
    final_img.save(out_path)
    print(f"Saved solid-color panoramic skyline (new source) to {out_path}")

except Exception as e:
    print(f"Error: {e}")
