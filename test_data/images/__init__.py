# test_data/images/__init__.py
# This makes 'images' a Python package
import os
from PIL import Image
import io

# Directory where test images are expected (if you put real ones there)
TEST_IMAGES_DIR = os.path.join(os.path.dirname(__file__))

def get_test_image_path(image_name):
    """Returns the full path to a test image."""
    return os.path.join(TEST_IMAGES_DIR, image_name)

def create_dummy_image(filepath, size=(100, 100), color=(0, 0, 0), max_bytes=None):
    """
    Creates a simple dummy JPEG image at the given filepath.
    Args:
        filepath (str or Path): The path where the image will be saved.
        size (tuple): (width, height) of the image.
        color (tuple): RGB tuple for the image color.
        max_bytes (int): If provided, will try to limit image size to this many bytes.
                        This is a rough estimate and might not be exact.
    """
    img = Image.new('RGB', size, color=color)

    # Try to save to a buffer first to check size
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=85) # Quality can impact size

    if max_bytes and img_byte_arr.tell() > max_bytes:
        # If too big, try to reduce quality or size (basic attempt)
        quality = 70
        while img_byte_arr.tell() > max_bytes and quality > 10:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=quality)
            quality -= 5
        if img_byte_arr.tell() > max_bytes:
            # If still too big, resize aggressively
            new_size = (size[0] // 2, size[1] // 2)
            img = Image.new('RGB', new_size, color=color)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)

    with open(filepath, 'wb') as f:
        f.write(img_byte_arr.getvalue())
    print(f"Created dummy image: {filepath} ({os.path.getsize(filepath)} bytes)")

# Example usage (for if you manually run this file, not typically done with fixtures)
if __name__ == "__main__":
    print("Creating example dummy images in test_data/images/")
    if not os.path.exists(TEST_IMAGES_DIR):
        os.makedirs(TEST_IMAGES_DIR)

    create_dummy_image(os.path.join(TEST_IMAGES_DIR, "tiny_test.jpg"), size=(10,10))
    create_dummy_image(os.path.join(TEST_IMAGES_DIR, "medium_test.jpg"), size=(100,100), color=(0, 255, 0))
    create_dummy_image(os.path.join(TEST_IMAGES_DIR, "large_test.jpg"), size=(500,500), color=(0, 0, 255))
    create_dummy_image(os.path.join(TEST_IMAGES_DIR, "extra_large_test.jpg"), size=(1500,1500), color=(255, 255, 0), max_bytes=100 * 1024) # ~100KB