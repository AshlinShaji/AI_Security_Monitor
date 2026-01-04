# ✅ STEP 7: Detect Objects Using YOLOv8
# This is where the AI looks at the image!

from ultralytics import YOLO
import cv2
import os

print("="*50)
print("🎯 STEP 7: Object Detection with YOLOv8")
print("="*50)

# Step A: Load the AI model
print("\n📥 Loading AI model (this takes 10-20 seconds first time)...")
model = YOLO("yolov8n.pt")
print("✅ Model loaded!")

# Step B: Load your image
image_path = "sample.jpg"

if os.path.exists(image_path):
    print(f"\n📷 Loading image: {image_path}")
    image = cv2.imread(image_path)
    print("✅ Image loaded!")
    
    # Step C: Run detection
    print("\n🔍 Analyzing image...")
    results = model(image)
    print("✅ Analysis complete!")
    
    # Step D: Show results
    print("\n📊 DETECTIONS FOUND:")
    print("-" * 50)
    
    for detection in results[0].boxes:
        class_id = int(detection.cls)
        class_name = results[0].names[class_id]
        confidence = float(detection.conf)
        
        # Show each detection
        print(f"✓ {class_name.upper():<15} | Confidence: {confidence*100:.1f}%")
    
    print("-" * 50)
    
    # Step E: Display image with boxes
    print("\n📺 Showing image with detection boxes...")
    results[0].show()
    
else:
    print(f"❌ Error: Cannot find {image_path}")