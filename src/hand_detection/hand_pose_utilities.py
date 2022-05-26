import copy, itertools
import moviepy.editor as mpy
import mediapipe as mp
import cv2 as cv
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def draw_keypoints(frame, frame_keypoints, predicted_class, position_top_left_corner = (20, 50), bgr_color=(255, 255, 255)):
    for keypoint in frame_keypoints:
        mp_drawing.draw_landmarks(frame, keypoint[0], mp_hands.HAND_CONNECTIONS, # access first item of the tuple since we want not pre-processed points
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        cv.putText(frame, 'Predicted class: ' + predicted_class['class'] + ' - confidence: ' + str(predicted_class['confidence']) + '%', position_top_left_corner,
               cv.FONT_HERSHEY_SIMPLEX, 0.6, bgr_color, 1, cv.LINE_AA)
    return frame

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list 

def calc_keypoints(frame, landmarks):
    image_width, image_height = frame.shape[1], frame.shape[0]
    landmark_point = []
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z # since we want to deal with 2D coordinates, Z is not processed.
        landmark_point.append([landmark_x, landmark_y, landmark_z])
    return pre_process_landmark(landmark_point)

