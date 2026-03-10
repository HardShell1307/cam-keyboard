import cv2
import mediapipe as mp
from pynput.keyboard import Controller
import math
import winsound

keyboard = Controller()

cap = cv2.VideoCapture(0)

# try higher resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

keys = [
["Q","W","E","R","T","Y","U","I","O","P"],
["A","S","D","F","G","H","J","K","L"],
["Z","X","C","V","B","N","M"]
]

cooldown = 0

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)

    h, w, c = frame.shape

    key_size = int(w/12)
    start_x = int(w*0.05)
    start_y = int(h*0.35)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_x, finger_y = None, None
    pinch = False

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            index_tip = hand.landmark[8]
            thumb_tip = hand.landmark[4]

            ix = int(index_tip.x * w)
            iy = int(index_tip.y * h)

            tx = int(thumb_tip.x * w)
            ty = int(thumb_tip.y * h)

            finger_x, finger_y = ix, iy

            # fingertip cursor
            cv2.circle(frame,(ix,iy),25,(0,255,255),2)
            cv2.circle(frame,(ix,iy),8,(0,255,0),-1)

            # thumb cursor
            cv2.circle(frame,(tx,ty),20,(255,200,0),2)
            cv2.circle(frame,(tx,ty),6,(255,120,0),-1)

            distance = math.hypot(ix-tx, iy-ty)

            if distance < 25:
                pinch = True
                cv2.line(frame,(ix,iy),(tx,ty),(0,255,0),3)

    for i in range(len(keys)):

        row = keys[i]
        offset = (10-len(row))*key_size//2

        for j in range(len(row)):

            x = start_x + offset + j*key_size
            y = start_y + i*key_size

            key = row[j]
            color = (255,80,80)

            if finger_x and finger_y:

                if x < finger_x < x+key_size and y < finger_y < y+key_size:

                    color = (0,255,0)

                    if pinch and cooldown == 0:

                        # type key
                        keyboard.press(key.lower())
                        keyboard.release(key.lower())

                        # terminal feedback
                        print("Key pressed:", key)

                        # keyboard click sound
                        winsound.Beep(1500,60)

                        cooldown = 10

                        cv2.rectangle(frame,(x,y),(x+key_size,y+key_size),(0,255,255),-1)

            cv2.rectangle(frame,(x,y),(x+key_size,y+key_size),color,2)

            cv2.putText(frame,key,
                        (x+int(key_size*0.3),y+int(key_size*0.7)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(255,255,255),2)

    if cooldown > 0:
        cooldown -= 1

    cv2.imshow("Cam Keyboard",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()