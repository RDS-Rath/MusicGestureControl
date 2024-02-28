import cv2
import mediapipe as mp
import pyautogui
import time

def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        cnt += 1

    return cnt

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

start_time = time.time()
continuous_volume_change = False
playpause_cooldown = False

prev = -1

while True:
    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]

        cnt = count_fingers(hand_keyPoints)

        if not (prev == cnt):
            # Reset continuous volume change flag
            continuous_volume_change = False

            if cnt == 2:
                pyautogui.press("volumeup")
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Volume Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            elif cnt == 1:
                pyautogui.press("volumedown")
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Volume Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            elif cnt == 3:
                pyautogui.press("nexttrack")
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Next Track", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            elif cnt == 4:
                pyautogui.press("prevtrack")
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Previous Track", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            elif cnt == 5 and not playpause_cooldown:
                pyautogui.press("playpause")
                playpause_cooldown = True
                start_time = time.time()
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Play/Pause", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            prev = cnt

        # Continuous volume change
        if continuous_volume_change:
            if cnt == 2:
                pyautogui.press("volumeup")
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Volume Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            elif cnt == 1:
                pyautogui.press("volumedown")
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS, landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4))
                cv2.putText(frm, "Volume Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Play/Pause cooldown
        if playpause_cooldown and (end_time - start_time) > 2:
            playpause_cooldown = False

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
