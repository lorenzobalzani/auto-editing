import copy, itertools
import moviepy.editor as mpy
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def draw_keypoints(video, keypoints, fps):
    frames = []
    for idx, frame in enumerate(video.iter_frames()):
        for keypoint in keypoints[idx]:
            mp_drawing.draw_landmarks(frame, keypoint[0], mp_hands.HAND_CONNECTIONS, # access first item of the tuple since we want not pre-processed points
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        frames.append(frame)
    return mpy.ImageSequenceClip(frames, fps=fps)


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

