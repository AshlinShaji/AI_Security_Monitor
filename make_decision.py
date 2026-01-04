# ✅ STEP 9: Make a Decision Based on Rules
# This is AGENTIC AI - the computer makes decisions!

from ultralytics import YOLO
import cv2
import os

print("="*50)
print("🎯 STEP 9: Making Decisions with Rules")
print("="*50)

# Load model
model = YOLO("yolov8n.pt")
image_path = "sample.jpg"

if os.path.exists(image_path):
    print(f"\n📷 Loading image: {image_path}")
    image = cv2.imread(image_path)
    
    # Run detection
    print("🔍 Detecting objects...")
    results = model(image)
    
    # Count people
    person_count = 0
    for detection in results[0].boxes:
        class_id = int(detection.cls)
        class_name = results[0].names[class_id]
        if class_name == "person":
            person_count += 1
    
    # ⭐ STEP 9A: APPLY RULES (This is where the AI thinks!)
    print("\n🤖 Applying decision rules...")
    
    # Rule 1: Check if crowded
    if person_count > 10:
        status = "🚨 VERY CROWDED"
        alert_level = "CRITICAL"
        action = "Evacuate area immediately!"
    elif person_count > 5:
        status = "⚠️  CROWDED"
        alert_level = "HIGH"
        action = "Monitor area carefully"
    elif person_count > 2:
        status = "✅ NORMAL"
        alert_level = "LOW"
        action = "Everything is fine"
    else:
        status = "📭 EMPTY"
        alert_level = "NONE"
        action = "Area is clear"
    
    # Show results
    print("\n📊 DECISION RESULTS:")
    print("="*50)
    print(f"👥 People Count: {person_count}")
    print(f"📊 Status: {status}")
    print(f"🚨 Alert Level: {alert_level}")
    print(f"📋 Recommended Action: {action}")
    print("="*50)
    
else:
    print(f"❌ Error: Cannot find {image_path}")