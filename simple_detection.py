# ✅ STEP 6: Load and Display an Image
# This is the FIRST part of our project!

from PIL import Image
import os

print("="*50)
print("🎯 STEP 6: Loading an Image")
print("="*50)

# Get the image file
image_path = "sample.jpg"  # Change this to your photo name

# Check if file exists
if os.path.exists(image_path):
    # Load the image
    my_photo = Image.open(image_path)
    print(f"✅ Image loaded successfully!")
    print(f"📏 Size: {my_photo.size} pixels")  # Shows width and height
    
    # Show the image
    my_photo.show()
    
else:
    print(f"❌ Error: Cannot find {image_path}")
    print("Make sure your image is in the same folder as this script!")