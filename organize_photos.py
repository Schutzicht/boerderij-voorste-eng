import os
import shutil

SOURCE_DIR = "/Users/jorikschut/Documents/Projecten-sites/Boerderij Voorste Eng/Fotos voorste eng"
DEST_BASE = "/Users/jorikschut/Documents/Projecten-sites/Boerderij Voorste Eng/public/images/real"

MAPPING = {
    "Fotos van buiten": "exterior",
    "fotos woonkamer": "living-room",
    "fotos slaapkamer": "bedroom",
    "fotos keuken": "kitchen",
    "fotos badkamer": "bathroom",
    "fotos van terras": "terrace",
    "fotos toilet": "toilet"
}

def organize_photos():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory not found: {SOURCE_DIR}")
        return

    # Create base destination directory
    if not os.path.exists(DEST_BASE):
        os.makedirs(DEST_BASE)

    total_files = 0
    
    for source_folder, dest_folder_name in MAPPING.items():
        source_path = os.path.join(SOURCE_DIR, source_folder)
        dest_path = os.path.join(DEST_BASE, dest_folder_name)
        
        if not os.path.exists(source_path):
            print(f"Warning: Source folder not found: {source_folder}")
            continue
            
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            
        # Get all files
        files = [f for f in os.listdir(source_path) if f.lower().endswith(('.avif', '.jpg', '.jpeg', '.png', '.webp'))]
        files.sort() # Ensure consistent order
        
        for i, filename in enumerate(files):
            ext = os.path.splitext(filename)[1].lower()
            new_filename = f"{dest_folder_name}-{i+1}{ext}"
            
            src_file = os.path.join(source_path, filename)
            dest_file = os.path.join(dest_path, new_filename)
            
            shutil.copy2(src_file, dest_file)
            print(f"Copied {filename} -> {dest_folder_name}/{new_filename}")
            total_files += 1

    print(f"Successfully processed {total_files} photos.")

if __name__ == "__main__":
    organize_photos()
