# ✅ STEP 8: Count People in the Image
# This is where we COUNT specific objects!

from ultralytics import YOLO
import cv2
import os

print("="*50)
print("🎯 STEP 8: Counting People")
print("="*50)

# Load model
print("\n📥 Loading AI model...")
model = YOLO("yolov8n.pt")

# Load image
image_path = "sample.jpg"

if os.path.exists(image_path):
    print(f"📷 Loading image: {image_path}")
    image = cv2.imread(image_path)
    
    # Run detection
    print("🔍 Detecting objects...")
    results = model(image)
    
    # Count people
    person_count = 0
    all_objects = []
    
    for detection in results[0].boxes:
        class_id = int(detection.cls)
        class_name = results[0].names[class_id]
        confidence = float(detection.conf)
        
        all_objects.append(class_name)
        
        if class_name == "person":
            person_count += 1
    
    # Show results
    print("\n📊 RESULTS:")
    print("-" * 50)
    print(f"👥 People detected: {person_count}")
    print(f"📦 Total objects found: {len(all_objects)}")
    print("\nAll objects:")
    
    for obj in all_objects:
        print(f"   • {obj}")
    
    print("-" * 50)
    
else:
    print(f"❌ Error: Cannot find {image_path}")