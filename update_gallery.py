import os
import subprocess

IMAGE_DIR = "matchdayimages"
INDEX_FILE = "index.html"
GALLERY_FILE = "gallery.html"

# Supported image extensions
EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG')

def get_git_commit_time(filepath):
    """
    Retrieves the epoch timestamp of when the image was last committed to Git.
    Falls back to file system modification time if Git history isn't available.
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", filepath],
            capture_output=True,
            text=True,
            check=True
        )
        timestamp = result.stdout.strip()
        if timestamp and timestamp.isdigit():
            return int(timestamp)
    except Exception:
        pass
    return os.path.getmtime(filepath)

def generate_grid_items(image_list):
    """Generates clean HTML grid items for the matchday photos."""
    items = []
    for img in image_list:
        items.append(
            f'    <div class="grid-item">\n'
            f'      <img src="{IMAGE_DIR}/{img}" alt="SRQ Gooners Matchday" loading="lazy">\n'
            f'    </div>'
        )
    return "\n".join(items)

def update_html_gallery(filename, grid_html):
    """Replaces content between GALLERY_START and GALLERY_END comments."""
    if not os.path.exists(filename):
        print(f"[-] Error: File '{filename}' not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- GALLERY_START -->"
    end_tag = "<!-- GALLERY_END -->"

    if start_tag not in content or end_tag not in content:
        print(f"[-] Warning: Missing '{start_tag}' or '{end_tag}' in {filename}.")
        return

    start_idx = content.find(start_tag) + len(start_tag)
    end_idx = content.find(end_tag)

    # Wrap the generated items inside the photo-grid container
    replacement_block = f'\n<div id="photo-grid" class="photo-grid">\n{grid_html}\n</div>\n'
    new_content = content[:start_idx] + replacement_block + content[end_idx:]

    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[+] Successfully updated {filename}")

def main():
    if not os.path.exists(IMAGE_DIR):
        print(f"[-] Directory '{IMAGE_DIR}' does not exist. Creating it now...")
        os.makedirs(IMAGE_DIR)
        return

    # Filter and sort images (newest committed files first)
    images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(EXTENSIONS)]
    images.sort(key=lambda img: get_git_commit_time(os.path.join(IMAGE_DIR, img)), reverse=True)

    if not images:
        print(f"[-] No matchday images found in '{IMAGE_DIR}'.")
        return

    print(f"[i] Found {len(images)} matchday image(s). Processing layout...")

    # Latest 3 images for the landing page (index.html)
    recent_images = images[:3]
    recent_grid_html = generate_grid_items(recent_images)

    # All images for the full gallery page (gallery.html)
    all_grid_html = generate_grid_items(images)

    # Apply updates
    update_html_gallery(INDEX_FILE, recent_grid_html)
    update_html_gallery(GALLERY_FILE, all_grid_html)

if __name__ == "__main__":
    main()
