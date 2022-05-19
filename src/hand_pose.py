import moviepy.editor as mpy
import mediapipe as mp
import argparse
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def draw_keypoints(video, keypoints, fps):
    frames = []
    for idx, frame in enumerate(video.iter_frames()):
        for keypoint in keypoints[idx]:
            mp_drawing.draw_landmarks(frame, keypoint, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        frames.append(frame)
    return mpy.ImageSequenceClip(frames, fps=fps)

def run_detection_hands(video, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    """Run hand gestures detection model using Google's Mediapipe

    Parameters:
    video (moviepy.editor.VideoFileClip): Input video
    model_complexity (Int): Complexity of the hand landmark model: 0 or 1. Landmark accuracy as well as inference latency generally go up with the model complexity. Default to 1.
    min_detection_confidence (Float): Minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. Default to 0.5.
    min_tracking_confidence (Float): Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the hand landmarks to be considered tracked successfully, or otherwise hand detection will be invoked automatically on the next input image. 

    Returns:
    List[List[landmark]]: A matrix of keypoints. Rows represent frames, columns represent detected 3D keypoints. 
   """
    keypoints = []
    with mp_hands.Hands(model_complexity=model_complexity, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence) as hands:
        for frame in video.iter_frames():
            frame_keypoints = hands.process(frame)
            if frame_keypoints.multi_hand_landmarks:
                keypoints.append([hand_landmarks for hand_landmarks in frame_keypoints.multi_hand_landmarks])
            else:
                keypoints.append([])
    return keypoints

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Help for hand pose detection.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--video", required=True, help="Path to the video.")
    args = vars(parser.parse_args())
    video = mpy.VideoFileClip(args['video'])
    keypoints = run_detection_hands(video)