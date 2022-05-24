import moviepy.editor as mpy
import mediapipe as mp
import argparse
from hand_detection.hand_pose_utilities import *
mp_hands = mp.solutions.hands

def run_detection_hands(video, draw_hands=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2):
    """Run hand gestures detection model using Google's Mediapipe

    Parameters:
    video (moviepy.editor.VideoFileClip): Input video
    model_complexity (Int): Complexity of the hand landmark model: 0 or 1. Landmark accuracy as well as inference latency generally go up with the model complexity. Default to 1.
    min_detection_confidence (Float): Minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. Default to 0.5.
    min_tracking_confidence (Float): Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the hand landmarks to be considered tracked successfully, or otherwise hand detection will be invoked automatically on the next input image. 
    max_num_hands (Int): Maximum number of hands to detect. Default to 2.

    Returns:
    List[List[Tuple(landmark, pre_processed_landmarks)]]: A matrix of keypoints. Rows represent frames, columns represent detected 3D keypoints. 
   """
    keypoints = []
    with mp_hands.Hands(model_complexity=model_complexity, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence, max_num_hands=max_num_hands) as hands:
        for time, frame in video.iter_frames(with_times = True):
            frame_keypoints = hands.process(frame)
            if frame_keypoints.multi_hand_landmarks:
                keypoints.append([(hand_landmarks, calc_keypoints(frame, hand_landmarks))
                    for hand_landmarks in frame_keypoints.multi_hand_landmarks])
            else:
                keypoints.append([])
            if draw_hands:
                frame = draw_keypoints(frame, keypoints[-1])
            # TODO: change video frame at time t
    return keypoints, video

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Help for hand pose detection.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--video", required=True, help="Path to the video.")
    args = vars(parser.parse_args())
    video = mpy.VideoFileClip(args['video'])
    keypoints = run_detection_hands(video)