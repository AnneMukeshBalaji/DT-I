import cv2
import mediapipe as mp
from pyzbar.pyzbar import decode
import pyttsx3

# Setup
engine = pyttsx3.init()
def speak(msg):
    print(f"[SPEAK] {msg}")
    engine.say(msg)
    engine.runAndWait()

# Init MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Function to detect QR and get its bounding box
def detect_qr(frame):
    qr_codes = decode(frame)
    for qr in qr_codes:
        x, y, w, h = qr.rect
        qr_data = qr.data.decode("utf-8")
        return True, (x, y, x + w, y + h), qr_data
    return False, None, None

# Check if any hand landmark is close to the QR bounding box
def is_hand_near_qr(hand_landmarks, qr_box, image_width, image_height):
    if not hand_landmarks or not qr_box:
        return False
    x1, y1, x2, y2 = qr_box
    for hand in hand_landmarks:
        for lm in hand.landmark:
            px, py = int(lm.x * image_width), int(lm.y * image_height)
            if x1 - 50 < px < x2 + 50 and y1 - 50 < py < y2 + 50:
                return True
    return False

# Main
cap = cv2.VideoCapture(0)
speak("AI scanning system activated.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_height, image_width, _ = frame.shape

    # QR Code detection
    qr_found, qr_box, qr_data = detect_qr(frame)
    if qr_found:
        x1, y1, x2, y2 = qr_box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "QR Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Hand detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    hand_landmarks = result.multi_hand_landmarks

    if hand_landmarks:
        for handLms in hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # Inference: scanning if hand is near QR
    scanning = qr_found and is_hand_near_qr(hand_landmarks, qr_box, image_width, image_height)
    if scanning:
        speak("Scanning QR code detected.")
        cv2.putText(frame, "SCANNING ✅", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.imwrite("qr_scan_detected.jpg", frame)
        break
    else:
        cv2.putText(frame, "Not scanning...", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("QR Scan Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        speak("Terminated by user.")
        break

cap.release()
cv2.destroyAllWindows()
