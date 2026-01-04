"""
🚨 AI SECURITY MONITOR
A complete project using Computer Vision, Agentic AI, and Generative AI!
"""

import streamlit as st
from ultralytics import YOLO
import cv2
import google.generativeai as genai
from PIL import Image
import numpy as np
import os

# ============================================================
# 🎨 PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="🚨 AI Security Monitor",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI Security Monitor")
st.write("Upload a photo and watch AI analyze it!")
st.write("---")

# ============================================================
# ⚙️ SETUP SECTION
# ============================================================
st.header("⚙️ Setup (Do this FIRST!)")

col1, col2 = st.columns(2)

with col1:
    api_key = st.text_input(
        "🔑 Enter your Google Gemini API Key:",
        type="password",
        help="Get it from https://aistudio.google.com/apikey"
    )

with col2:
    st.info("📌 Need an API key? Go to https://aistudio.google.com/apikey")

if not api_key:
    st.warning("⚠️ Please enter your API key above to use the report generator!")
else:
    st.success("✅ API Key accepted!")

# ============================================================
# 📷 IMAGE UPLOAD
# ============================================================
st.header("📷 Step 1: Upload Image")
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"],
    help="Upload a photo to analyze"
)

if uploaded_file is not None:
    # ========================================================
    # Display uploaded image
    # ========================================================
    st.subheader("Your Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    # Convert to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # ========================================================
    # 🔍 STEP 2: OBJECT DETECTION
    # ========================================================
    st.header("🔍 Step 2: Detecting Objects (Computer Vision)")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("📥 Loading AI model...")
    progress_bar.progress(25)
    
    model = YOLO("yolov8n.pt")
    
    status_text.text("🔍 Analyzing image...")
    progress_bar.progress(50)
    
    results = model(image_cv)
    
    status_text.text("✅ Detection complete!")
    progress_bar.progress(100)
    
    # Get all detections
    all_detections = []
    for detection in results[0].boxes:
        class_id = int(detection.cls)
        class_name = results[0].names[class_id]
        confidence = float(detection.conf)
        all_detections.append({
            "object": class_name.upper(),
            "confidence": f"{confidence*100:.1f}%"
        })
    
    # Display detections
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Objects Found:**")
        for i, det in enumerate(all_detections, 1):
            st.write(f"{i}. {det['object']} ({det['confidence']})")
    
    with col2:
        st.metric("Total Objects", len(all_detections))
    
    # ========================================================
    # 👥 STEP 3: COUNT PEOPLE
    # ========================================================
    st.header("👥 Step 3: Counting People (Agentic AI)")
    
    person_count = 0
    for detection in results[0].boxes:
        class_id = int(detection.cls)
        class_name = results[0].names[class_id]
        if class_name == "person":
            person_count += 1
    
    st.metric("People Detected", person_count)
    
    # ========================================================
    # 🤖 STEP 4: MAKE DECISION
    # ========================================================
    st.header("🤖 Step 4: Making Decision (Agentic AI)")
    
    if person_count > 10:
        status = "🚨 VERY CROWDED"
        alert_level = "CRITICAL"
        color = "red"
        action = "Evacuate area immediately!"
    elif person_count > 5:
        status = "⚠️  CROWDED"
        alert_level = "HIGH"
        color = "orange"
        action = "Monitor area carefully"
    elif person_count > 2:
        status = "✅ NORMAL"
        alert_level = "LOW"
        color = "green"
        action = "Everything is fine"
    else:
        status = "📭 EMPTY"
        alert_level = "NONE"
        color = "blue"
        action = "Area is clear"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", status)
    with col2:
        st.metric("Alert Level", alert_level)
    with col3:
        st.metric("Action", action)
    
    # ========================================================
    # 📝 STEP 5: GENERATE REPORT
    # ========================================================
    st.header("📝 Step 5: Generating Report (Generative AI)")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        prompt = f"""
        You are a friendly security report writer.
        
        INFORMATION:
        - People detected: {person_count}
        - Status: {status}
        - Alert Level: {alert_level}
        - Recommended Action: {action}
        
        TASK: Write a SHORT, friendly report (exactly 3 sentences) 
        about this situation. Write like you're talking to a 10-year-old.
        Make it helpful and clear!
        """
        
        try:
            # Try different models in order
            models_to_try = [
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-pro",
            ]
            
            report = None
            for model_name in models_to_try:
                try:
                    model_gemini = genai.GenerativeModel(model_name)
                    response = model_gemini.generate_content(prompt)
                    report = response.text
                    break
                except:
                    continue
            
            if report:
                st.success("✅ Report Generated!")
                st.info(report)
            else:
                st.warning("⚠️ Could not generate report. Try uploading a different image.")
            
        except Exception as e:
            st.error(f"❌ Error generating report: {e}")
            st.info("Try updating: pip install --upgrade google-generativeai")
    
    # ========================================================
    # 🎨 SHOW ANNOTATED IMAGE
    # ========================================================
    st.header("🎨 Annotated Image (with Detection Boxes)")
    
    annotated_image = results[0].plot()
    annotated_pil = Image.fromarray(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
    st.image(annotated_pil, use_column_width=True, caption="AI detected these boxes")
    
    # ========================================================
    # 📊 SUMMARY
    # ========================================================
    st.header("📊 Summary")
    summary = f"""
    **Analysis Complete!**
    
    - ✅ Objects detected: {len(all_detections)}
    - 👥 People found: {person_count}
    - 📊 Status: {status}
    - 🚨 Alert: {alert_level}
    - 📋 Action: {action}
    """
    st.success(summary)

else:
    st.info("👆 Upload an image to get started!")