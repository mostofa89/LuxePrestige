"""
Generate placeholder images for product gallery
Creates simple placeholder images with product names and colors
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Image configuration
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 800
BACKGROUND_COLORS = {
    'main': '#E8E3DA',      # Moon white
    'detail': '#D4C5B9',    # Pearl
    'lifestyle': '#C9A797', # Rose gold tint
    'side': '#D4C5B9',
    'closeup': '#C9A797',
    'wear': '#E8E3DA',
    'texture': '#D4C5B9',
    'layered': '#C9A797',
}

# Product image definitions from fixture
IMAGES = [
    'solstice-chain-main.jpg',
    'solstice-chain-detail.jpg',
    'solstice-chain-lifestyle.jpg',
    'nocturne-band-main.jpg',
    'nocturne-band-side.jpg',
    'halo-studs-main.jpg',
    'halo-studs-closeup.jpg',
    'halo-studs-wear.jpg',
    'sable-cuff-main.jpg',
    'sable-cuff-texture.jpg',
    'aurora-charm-main.jpg',
    'aurora-charm-layered.jpg',
    'lumina-drops-main.jpg',
    'veil-pendant-main.jpg',
    'veil-pendant-detail.jpg',
    'echo-hoops-main.jpg',
    'frost-signet-main.jpg',
    'dusk-chain-main.jpg',
    'dusk-chain-closeup.jpg',
    'aurora-charm-detail.jpg',
]

def get_background_color(filename):
    """Get background color based on image type"""
    for key, color in BACKGROUND_COLORS.items():
        if key in filename:
            return color
    return '#E8E3DA'  # Default moon white

def create_placeholder_image(filename, output_path):
    """Create a placeholder image with text"""
    # Create image with background color
    bg_color = get_background_color(filename)
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Extract product name and type from filename
    parts = filename.replace('.jpg', '').split('-')
    product_name = ' '.join(parts[:-1]).title()
    image_type = parts[-1].title()
    
    # Try to use a nice font, fallback to default
    try:
        # Try different font sizes for product name and type
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Calculate text positions (centered)
    text_color = '#2C2C2C'  # Obsidian dark
    
    # Draw product name
    bbox1 = draw.textbbox((0, 0), product_name, font=font_large)
    text_width1 = bbox1[2] - bbox1[0]
    text_height1 = bbox1[3] - bbox1[1]
    x1 = (IMAGE_WIDTH - text_width1) // 2
    y1 = (IMAGE_HEIGHT - text_height1) // 2 - 40
    
    draw.text((x1, y1), product_name, fill=text_color, font=font_large)
    
    # Draw image type
    bbox2 = draw.textbbox((0, 0), image_type, font=font_small)
    text_width2 = bbox2[2] - bbox2[0]
    text_height2 = bbox2[3] - bbox2[1]
    x2 = (IMAGE_WIDTH - text_width2) // 2
    y2 = y1 + text_height1 + 20
    
    draw.text((x2, y2), image_type, fill=text_color, font=font_small)
    
    # Draw decorative border
    border_color = '#C9A797'  # Rose gold
    draw.rectangle(
        [(20, 20), (IMAGE_WIDTH - 20, IMAGE_HEIGHT - 20)],
        outline=border_color,
        width=3
    )
    
    # Draw corner ornaments (simple lines)
    corner_size = 50
    # Top-left
    draw.line([(20, 20), (20 + corner_size, 20)], fill=border_color, width=3)
    draw.line([(20, 20), (20, 20 + corner_size)], fill=border_color, width=3)
    # Top-right
    draw.line([(IMAGE_WIDTH - 20, 20), (IMAGE_WIDTH - 20 - corner_size, 20)], fill=border_color, width=3)
    draw.line([(IMAGE_WIDTH - 20, 20), (IMAGE_WIDTH - 20, 20 + corner_size)], fill=border_color, width=3)
    # Bottom-left
    draw.line([(20, IMAGE_HEIGHT - 20), (20 + corner_size, IMAGE_HEIGHT - 20)], fill=border_color, width=3)
    draw.line([(20, IMAGE_HEIGHT - 20), (20, IMAGE_HEIGHT - 20 - corner_size)], fill=border_color, width=3)
    # Bottom-right
    draw.line([(IMAGE_WIDTH - 20, IMAGE_HEIGHT - 20), (IMAGE_WIDTH - 20 - corner_size, IMAGE_HEIGHT - 20)], fill=border_color, width=3)
    draw.line([(IMAGE_WIDTH - 20, IMAGE_HEIGHT - 20), (IMAGE_WIDTH - 20, IMAGE_HEIGHT - 20 - corner_size)], fill=border_color, width=3)
    
    # Save image
    img.save(output_path, 'JPEG', quality=85)
    print(f"Created: {filename}")

def main():
    """Generate all placeholder images"""
    # Create output directory
    output_dir = Path('media/product_images')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {len(IMAGES)} placeholder images...")
    print(f"Output directory: {output_dir.absolute()}")
    print("-" * 50)
    
    # Generate each image
    for filename in IMAGES:
        output_path = output_dir / filename
        create_placeholder_image(filename, output_path)
    
    print("-" * 50)
    print(f"✓ Successfully generated {len(IMAGES)} images")
    print(f"✓ Location: {output_dir.absolute()}")

if __name__ == '__main__':
    main()
