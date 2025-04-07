import cv2
import time
import google.generativeai as genai
from PIL import Image
import numpy as np
from google.api_core.exceptions import ResourceExhausted
import re

# Configure Gemini
genai.configure(api_key="AIzaSyAPqvDcQepWJN1RcQrcrbVhGbm7BwImibk")
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("🚀 Starting AI QR Code Scan Detection...")

# Capture only every 12 seconds = 5 photos per minute
CAPTURE_INTERVAL = 12
last_capture_time = 0
last_result = None
retry_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        # Show the live webcam feed
        cv2.imshow("📸 QR Code Scan Detection", frame)

        current_time = time.time()
        if current_time - last_capture_time >= CAPTURE_INTERVAL:
            last_capture_time = current_time

            # Convert OpenCV image to PIL
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            prompt = "Is the person scanning a QR code or making a payment? Respond with just: 'Payment done' or 'Payment not done'."

            print("🧠 Sending image to Gemini...")

            try:
                response = model.generate_content([prompt, image])
                result = response.text.strip()

                if result != last_result:
                    print(f"✅ Gemini Response: {result}")
                    last_result = result
                else:
                    print("ℹ️ Same result as last time.")

                retry_count = 0

            except ResourceExhausted as e:
                print("⚠️ Rate limit hit!")

                # Extract or fallback to exponential backoff
                match = re.search(r'retry_delay\s*{\s*seconds:\s*(\d+)', str(e))
                delay_seconds = int(match.group(1)) if match else (2 ** retry_count)
                delay_seconds = min(delay_seconds, 120)

                print(f"⏳ Waiting {delay_seconds} seconds before retry...")
                time.sleep(delay_seconds)
                retry_count += 1
                continue

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Webcam closed.")
