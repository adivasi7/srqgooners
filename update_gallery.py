import os
import subprocess

IMAGE_DIR = "matchdayimages"
INDEX_FILE = "index.html"
GALLERY_FILE = "gallery.html"

extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG')
images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(extensions)]

def get_git_file_time(filepath):
    """Gets the timestamp of when the file was last committed in Git."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", filepath],
            capture_output=True,
            text=True,
            check=True
        )
        timestamp = result.stdout.strip()
        return int(timestamp) if timestamp else os.path.getmtime(filepath)
    except Exception:
        return os.path.getmtime(filepath)

# Sort images by Git commit timestamp (newest first)
images.sort(key=lambda x: get_git_file_time(os.path.join(IMAGE_DIR, x)), reverse=True)

# Generate HTML grids
recent_images = images[:3]

recent_grid_html = ""
for img in recent_images:
    recent_grid_html += f'    <div class="grid-item"><img src="{IMAGE_DIR}/{img}" alt="SRQ Gooners Matchday" loading="lazy"></div>\n'

all_grid_html = ""
for img in images:
    all_grid_html += f'    <div class="grid-item"><img src="{IMAGE_DIR}/{img}" alt="SRQ Gooners Matchday" loading="lazy"></div>\n'

def update_file(filename, grid_content):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_tag = ""
    end_tag = ""
    
    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        new_content = content[:start_idx] + f'\n<div id="photo-grid" class="photo-grid">\n{grid_content}</div>\n' + content[end_idx:]
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Successfully updated {filename}")
    else:
        print(f"Warning: {start_tag} and {end_tag} tags not found in {filename}")

update_file(INDEX_FILE, recent_grid_html)
update_file(GALLERY_FILE, all_grid_html)
