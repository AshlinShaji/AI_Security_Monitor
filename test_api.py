import google.generativeai as genai

# Test your API key
API_KEY = "AIzaSyDqyIF0EDH0oa6pcPIzKbK8OSh36JfCz_s"  # Add your key here!

print("Testing API key...")
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say hello!")
    print("✅ API Key works!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")