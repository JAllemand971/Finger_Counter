import cv2
import mediapipe as mp

# === Initialize MediaPipe Hands module ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Detect at most one hand
mp_draw = mp.solutions.drawing_utils     # To draw hand landmarks

# === Start the webcam ===
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    # === Copy of the image to overlay a transparent red filter if needed ===
    overlay = img.copy()  # We'll draw on top of this image

    # === Convert from BGR (OpenCV) to RGB (MediaPipe expects RGB) ===
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # By default: we don't display the red filter
    show_red_filter = False

    # === If a hand is detected ===
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # --- Get the list of landmarks (hand key points) ---
            landmarks = hand_landmarks.landmark
            finger_tips = [4, 8, 12, 16, 20]
            fingers = []

            # --- Fix hand label because of mirrored webcam image ---
            raw_label = results.multi_handedness[i].classification[0].label
            hand_label = "Left" if raw_label == "Right" else "Right"

            # --- Detect thumb (X axis, horizontal movement) ---
            if hand_label == "Right":
                fingers.append(1 if landmarks[4].x > landmarks[3].x else 0)
            else:  # Left
                fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)

            # --- Detect other 4 fingers (Y axis, vertical movement) ---
            for tip_id in finger_tips[1:]:
                fingers.append(1 if landmarks[tip_id].y < landmarks[tip_id - 2].y else 0)

            # --- Count how many fingers are up ---
            total_fingers = sum(fingers)

            # --- Display the number of fingers up ---
            cv2.putText(img, f'Fingers: {total_fingers}', (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

            # --- Display the corrected hand label ---
            cv2.putText(img, f'Hand: {hand_label}', (20, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            # === If combination is [1,1,0,0,1] (thumb + index + pinky up) ===
            if fingers == [1, 1, 0, 0, 1]:
                show_red_filter = True

    # === Add a transparent red filter if condition is met ===
    if show_red_filter:
        alpha = 0.4  # Transparency level (0 = fully transparent, 1 = fully opaque)
        red_color = (0, 0, 255)  # Red in BGR
        overlay[:] = red_color   # Fill overlay with red
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)  # Blend overlay with webcam feed
        # Show warning message
        cv2.putText(img, "AMAZING", (50, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)

    # === Show the final image in a window ===
    cv2.imshow("Hand detection", img)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
