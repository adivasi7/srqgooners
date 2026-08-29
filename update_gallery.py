import os

IMAGE_DIR = "matchdayimages"
INDEX_FILE = "index.html"
GALLERY_FILE = "gallery.html"

# Get all images sorted by last modified time (newest first)
extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG')
images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(extensions)]
images.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIR, x)), reverse=True)

# Generate HTML grids
recent_images = images[:3]

recent_grid_html = ""
for img in recent_images:
    recent_grid_html += f'  <div class="grid-item"><img src="{IMAGE_DIR}/{img}" alt="SRQ Gooners Matchday"></div>\n'

all_grid_html = ""
for img in images:
    all_grid_html += f'  <div class="grid-item"><img src="{IMAGE_DIR}/{img}" alt="SRQ Gooners Matchday"></div>\n'

def update_file(filename, grid_content):
    if not os.path.exists(filename):
        return
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_tag = "<!-- GALLERY_START -->"
    end_tag = "<!-- GALLERY_END -->"
    
    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        new_content = content[:start_idx] + f'\n<div id="photo-grid" class="photo-grid">\n{grid_content}</div>\n' + content[end_idx:]
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)

update_file(INDEX_FILE, recent_grid_html)
update_file(GALLERY_FILE, all_grid_html)
print(f"Successfully updated {INDEX_FILE} (3 latest) and {GALLERY_FILE} (all {len(images)} photos).")
