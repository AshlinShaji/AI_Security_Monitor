# ✅ STEP 10: Generate a Report with Google Gemini (FIXED VERSION)
# Uses NEW google-genai SDK (SUPPORTED)

from ultralytics import YOLO
import cv2
import os
from google import genai

print("=" * 50)
print("🎯 STEP 10: Generating Report with Gemini")
print("=" * 50)

# 🔐 Load API key securely
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found!")
    print("💡 Set it using:")
    print('   setx GEMINI_API_KEY "YOUR_API_KEY"')
    exit()

print("✅ Gemini API key loaded securely")

# 🤖 Initialize Gemini client
client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1"}
)

print("✅ Gemini connected!")

# 📥 Load YOLO model
print("\n📥 Loading YOLO model...")
model = YOLO("yolov8n.pt")

# 📷 Image path
image_path = "sample.jpg"

if not os.path.exists(image_path):
    print(f"❌ Error: Cannot find {image_path}")
    exit()

print(f"📷 Loading image: {image_path}")
image = cv2.imread(image_path)

# 🔍 Run detection
print("🔍 Detecting objects...")
results = model(image)

# 👥 Count people
person_count = 0
for box in results[0].boxes:
    class_id = int(box.cls)
    class_name = results[0].names[class_id]
    if class_name == "person":
        person_count += 1

# 📊 Decide area status
status = "CROWDED" if person_count > 5 else "NORMAL"

# 📝 Create prompt
print("\n📝 Creating prompt for Gemini...")
prompt = f"""
You are a friendly security report writer.

INFORMATION:
- Number of people detected: {person_count}
- Area status: {status}

TASK:
Write EXACTLY 3 short sentences.
Write like you are explaining to a 10-year-old.
Keep it simple, calm, and helpful.
"""

print("🤖 Asking Gemini to write a report...")

try:
    response = client.models.generate_content(
        model="gemini-pro",
        contents=prompt
    )

    report = response.text

    print("\n" + "=" * 50)
    print("📊 SECURITY REPORT")
    print("=" * 50)
    print(f"👥 People Detected : {person_count}")
    print(f"📊 Area Status   : {status}")
    print("🤖 Model Used    : gemini-pro")
    print("\n📝 AI-Generated Report:")
    print("-" * 50)
    print(report)
    print("-" * 50)
    print("\n✨ Report generated successfully!")

except Exception as e:
    print("\n❌ Failed to generate report")
    print(f"🔍 Error: {e}")
