# ✅ STEP 10: Generate a Report with OpenAI GPT-4/GPT-4o
# FREE TRIAL: Get $5 free credits at https://platform.openai.com

from ultralytics import YOLO
import cv2
import os

print("="*50)
print("🎯 STEP 10: Generating Report with OpenAI")
print("="*50)

# ⭐ GET YOUR FREE API KEY FROM: https://platform.openai.com
API_KEY = ""  # sk-proj-...

if API_KEY == "YOUR_OPENAI_API_KEY_HERE":
    print("❌ ERROR: You need to add your OpenAI API key!")
    print("📚 Steps to get FREE API key:")
    print("   1. Go to https://platform.openai.com")
    print("   2. Sign up (free)")
    print("   3. Go to API keys section")
    print("   4. Create new secret key")
    print("   5. Copy and paste it here")
    print("\n💡 New accounts get $5 FREE CREDITS!")
    exit()

# Import OpenAI
try:
    from openai import OpenAI
    print("✅ OpenAI library found!")
except ImportError:
    print("Installing OpenAI library...")
    import subprocess
    subprocess.check_call(["pip", "install", "openai"])
    from openai import OpenAI

# Create OpenAI client
client = OpenAI(api_key=API_KEY)
print("✅ OpenAI connected!")

# Load YOLO model
print("\n📥 Loading YOLO model...")
model = YOLO("yolov8n.pt")

image_path = "sample.jpg"

if os.path.exists(image_path):
    print(f"📷 Loading image: {image_path}")
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
    
    # Make decision
    if person_count > 5:
        status = "CROWDED"
    else:
        status = "NORMAL"
    
    # Create a prompt
    print("\n📝 Creating prompt for GPT-4...")
    prompt = f"""You are a friendly security report writer.

INFORMATION:
- Number of people detected: {person_count}
- Area status: {status}

TASK: Write a SHORT, friendly report (exactly 3 sentences) about this situation. 
Write like you're talking to a 10-year-old. Keep it simple and helpful!"""
    
    # Ask GPT-4 to write the report
    print("🤖 Asking GPT-4 to write a report...")
    try:
        # Try GPT-4 first (most capable)
        # If quota exceeded, it automatically falls back to GPT-4o mini
        models_to_try = [
            "gpt-4",           # Most capable
            "gpt-4-turbo",     # Fast
            "gpt-4o",          # Latest
            "gpt-3.5-turbo",   # Cheap/fast
        ]
        
        report = None
        used_model = None
        
        for model_name in models_to_try:
            try:
                print(f"   Trying {model_name}...")
                
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                
                report = response.choices[0].message.content
                used_model = model_name
                print(f"   ✅ Success with {model_name}!")
                break
                
            except Exception as e:
                error_str = str(e).lower()
                if "rate_limit" in error_str or "quota" in error_str:
                    print(f"   ❌ {model_name}: Quota exceeded, trying next...")
                    continue
                elif "not found" in error_str or "does not exist" in error_str:
                    print(f"   ❌ {model_name}: Not available, trying next...")
                    continue
                else:
                    print(f"   ❌ {model_name}: Error - {str(e)[:50]}...")
                    continue
        
        if report:
            # Show results
            print("\n" + "="*50)
            print("📊 SECURITY REPORT")
            print("="*50)
            print(f"👥 People Detected: {person_count}")
            print(f"📊 Status: {status}")
            print(f"✅ Model Used: {used_model} (OpenAI)")
            print("\n📝 AI-Generated Report:")
            print("-"*50)
            print(report)
            print("-"*50)
            print("\n✨ Report generated successfully!")
            print(f"\n💡 Check your usage: https://platform.openai.com/account/usage/overview")
        else:
            print("\n❌ Could not generate report with any model")
            print("\n💡 SOLUTIONS:")
            print("   1. Check your API key is correct")
            print("   2. Make sure you have credits: https://platform.openai.com/account/billing/overview")
            print("   3. Try again in a few moments")
    
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}")
        
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            print("\n⚠️  Invalid API key!")
            print("💡 Get a new key: https://platform.openai.com/api-keys")
        elif "429" in error_msg or "rate_limit" in error_msg.lower():
            print("\n⚠️  Rate limit exceeded!")
            print("💡 Wait a few moments and try again")
        elif "insufficient_quota" in error_msg.lower():
            print("\n⚠️  No API credits available!")
            print("💡 Check your account: https://platform.openai.com/account/billing/overview")
            print("   New accounts get $5 free!")
        else:
            print("\n💡 First time setup:")
            print("   1. pip install openai")
            print("   2. Get API key: https://platform.openai.com")
            print("   3. Add key to this script")

else:
    print(f"❌ Error: Cannot find {image_path}")