<h1>Finger Counter</h1>
Real-time hand tracking and **finger counting** in Python using **MediaPipe** and **OpenCV**.


<h2>Demo</h2>

  <table align="center">
  <tr>
    <th>Titre</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Counting Fingers</td>
    <td>

https://github.com/user-attachments/assets/622fb692-150b-47f9-91b3-b7598cf5c809
      
  </tr>
  </table>

## What it does

- Captures webcam frames with **OpenCV**
- Detects a hand and **21 landmarks** with **MediaPipe Hands**
- Classifies each finger as **extended** or **folded**
- Displays the **count** and the annotated hand overlay in real time

MediaPipe Hands returns 21 (x, y, z) landmarks and handedness (left vs. right), enabling robust fingertip and joint reasoning. :contentReference[oaicite:1]{index=1}

---

## How it works (pipeline)

1. **Capture**  
   `cv2.VideoCapture(0)` grabs frames from the default camera. Frames are flipped if desired for “mirror” UX.

2. **Landmark detection**  
   MediaPipe Hands processes the `RGB` frame and returns:
   - `multi_hand_landmarks`: 21 keypoints per detected hand  
   - `multi_handedness`: label `"Left"` or `"Right"` with confidence  
   (Both are used to normalize rules for the thumb vs. other fingers.) :contentReference[oaicite:2]{index=2}

3. **Finger state rules**  
   A common, fast heuristic:
   - **Index, Middle, Ring, Pinky**: tip is above its PIP joint in image coordinates (remember y grows downward in images).  
     Example (index): `tip = 8`, `pip = 6` → `extended = (y_tip < y_pip)`
   - **Thumb**: check **x** direction relative to IP joint and **handedness**  
     - Right hand: `x_tip > x_ip` ⇒ extended  
     - Left hand:  `x_tip < x_ip` ⇒ extended  
   Sum of `extended` booleans gives the **count**.

4. **Visualization**  
   - Draw landmarks and connections on the frame
   - Put the current count (e.g., `cv2.putText`) in the top-left corner
   - Show the annotated frame via `cv2.imshow("Finger Counter", frame)`

> Note: You can also use angle-based rules (vector dot products between finger segments) for higher robustness, but the simple tip-vs-pip check is fast and effective for a demo.


