from PIL import Image, ImageOps
import numpy as np
import os

# Source path
src_path = "/Users/jorikschut/.gemini/antigravity/brain/edce318d-ef0c-4e17-90b4-6466e53cb62d/uploaded_image_1768581801516.png"
out_path = "/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-panorama.png"

try:
    img = Image.open(src_path).convert("RGBA")
    print(f"Original Dimensions: {img.size}")

    # 1. UPSCALE FIRST (Max Quality)
    # Upscaling the raw image first allows us to threshold the edges at high resolution,
    # ensuring a much sharper, vector-like result than upscaling a low-res mask.
    target_scale = 4.0 
    new_w = int(img.width * target_scale)
    new_h = int(img.height * target_scale)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    print(f"Upscaled Dimensions: {img.size}")

    # 2. COLORIZE & REMOVE BACKGROUND (High Res)
    data = np.array(img)
    
    # Target Blue #0e4c92
    target_blue = [14, 76, 146] 
    
    # Threshold at 240
    threshold = 240 
    
    r = data[:, :, 0]
    g = data[:, :, 1]
    b = data[:, :, 2]
    # Keep alpha check in case source had transparency
    a = data[:, :, 3]
    
    is_not_white = (r < threshold) | (g < threshold) | (b < threshold)
    has_alpha = (a > 20)
    
    content_mask = is_not_white & has_alpha
    
    # Create new buffer
    new_data = np.zeros_like(data)
    
    # Apply solid blue
    new_data[content_mask, 0] = target_blue[0]
    new_data[content_mask, 1] = target_blue[1]
    new_data[content_mask, 2] = target_blue[2]
    new_data[content_mask, 3] = 255
    
    img = Image.fromarray(new_data)
    
    # 3. Trim whitespace (Crop)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f"Cropped High-Res Content: {bbox} -> {img.size}")
    
    # 4. Create Panorama (Mirroring)
    # Using 4 tiles to be safe with coverage
    img_flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    img_arr = np.array(img)
    img_flipped_arr = np.array(img_flipped)
    
    # Pattern: Flip | Original | Flip | Original
    combined_arr = np.hstack([img_flipped_arr, img_arr, img_flipped_arr, img_arr])
    
    # 5. Save
    final_img = Image.fromarray(combined_arr)
    final_img.save(out_path)
    print(f"Saved sharp solid-color panorama to {out_path}")

except Exception as e:
    print(f"Error: {e}")
