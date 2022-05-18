import moviepy.editor as mpy
import mediapipe as mp
mp_hands = mp.solutions.hands

def extract_hands_keypoints(hands, frame):
    return hands.process(frame)

def run_detection_hands(video):
    """Run hand gestures detection model using Google's Mediapipe

    Parameters:
    video (moviepy.editor.VideoFileClip): Input video

    Returns:
    List[List[landmark]]: A matrix of keypoints. Rows represent frames, columns represent detected 3D keypoints. 
   """
    keypoints = []
    with mp_hands.Hands(model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        for frame in video.iter_frames():
            frame_keypoints = extract_hands_keypoints(hands, frame)
            if frame_keypoints.multi_hand_landmarks:
                keypoints.append([hand_landmarks for hand_landmarks in frame_keypoints.multi_hand_landmarks])
    return keypoints

if __name__ == '__main__':
    video = mpy.VideoFileClip('video.mov')
    keypoints = run_detection_hands(video)