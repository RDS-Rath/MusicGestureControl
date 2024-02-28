import cv2
import mediapipe as mp
import pyautogui

# Initialize hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Variables for volume control
current_volume = pyautogui.volume()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # Get landmarks for the first hand
        hand_landmarks = results.multi_hand_landmarks[0].landmark

        # Get coordinates of specific landmarks (adjust these based on your hand position)
        thumb_tip = hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        palm = hand_landmarks[mp_hands.HandLandmark.PALM]

        # Calculate the distance between index and middle finger tips
        finger_distance = ((index_tip.x - middle_tip.x) ** 2 + (index_tip.y - middle_tip.y) ** 2) ** 0.5

        # Previous song/media
        if finger_distance > 0.1 and index_tip.x < middle_tip.x:
            pyautogui.press('media_previous')

        # Next song/media
        elif finger_distance > 0.1 and index_tip.x > middle_tip.x:
            pyautogui.press('media_next')

        # Pause/play
        elif finger_distance < 0.05 and thumb_tip.y < index_tip.y < middle_tip.y:
            pyautogui.press('space')

        # Stop music
        elif palm.y < index_tip.y and palm.y < middle_tip.y:
            pyautogui.press('stop')

        # Volume control
        elif palm.y > index_tip.y and palm.y > middle_tip.y:
            if index_tip.y > middle_tip.y:
                # Increase volume
                pyautogui.press('volumeup')
            else:
                # Decrease volume
                pyautogui.press('volumedown')

    # Display the frame
    cv2.imshow('Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
