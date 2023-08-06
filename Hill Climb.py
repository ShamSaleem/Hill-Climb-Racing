import cv2
import mediapipe as mp
import pyautogui as pya

pya.PAUSE = 0

mphands = mp.solutions.hands
hands = mphands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 650)
cap.set(4, 650)

ret, frame = cap.read()
frame = cv2.flip(frame, 1)

h, w, c = frame.shape

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
            # Check if it's the right hand based on wrist position
            if handLMs.landmark[mphands.HandLandmark.WRIST].x > handLMs.landmark[
                mphands.HandLandmark.INDEX_FINGER_TIP
            ].x:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                for lm in handLMs.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y
                cv2.rectangle(
                    frame,
                    (x_min - 20, y_min - 20),
                    (x_max + 20, y_max + 20),
                    (0, 255, 0),
                    2,
                )
                mp_drawing.draw_landmarks(
                    frame, handLMs, mphands.HAND_CONNECTIONS
                )

                # Add text above the bounding box
                if handLMs.landmark[mphands.HandLandmark.THUMB_TIP].x > handLMs.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].x:
                    pya.keyDown("Left")
                    pya.keyUp("Right")
                    cv2.putText(frame, "Brake", (x_min, y_min - 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
                else:
                    pya.keyDown("Right")
                    pya.keyUp("Left")
                    cv2.putText(frame, "Accelerate", (x_min, y_min - 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)

        # Get and display FPS in the corner
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
