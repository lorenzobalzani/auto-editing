import datetime
import moviepy.editor as mpy
import numpy as np
import mediapipe as mp
import argparse
from gestures import Gestures
from hand_detection.hand_pose_utilities import *
from hand_detection.model_config import *
import tensorflow as tf
mp_hands = mp.solutions.hands

def run_detection_hands(video, 
                        classification_model_path, 
                        available_gestures_path, 
                        draw_hands=False, 
                        model_complexity=1,
                        min_detection_confidence=0.5, 
                        min_tracking_confidence=0.5, 
                        max_num_hands=2):
    '''Run hand gestures detection model using Google's Mediapipe

    Parameters:
    video (moviepy.editor.VideoFileClip): input video.
    classification_model_path (String): path to TF classification model.
    available_gestures_path (String): path to CSV that includes gestures.
    model_complexity (Int): complexity of the hand landmark model: 0 or 1. Landmark accuracy as well as inference latency generally go up with the model complexity. Default to 1.
    min_detection_confidence (Float): minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. Default to 0.5.
    min_tracking_confidence (Float): minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the hand landmarks to be considered tracked successfully, or otherwise hand detection will be invoked automatically on the next input image. 
    max_num_hands (Int): maximum number of hands to detect. Default to 2.

    Returns:
    List[List[Tuple(landmark, pre_processed_landmarks)]]: matrix of keypoints. Rows represent frames, columns represent detected 3D keypoints. 
   '''
    to_draw = {'keypoints': {}, 'classes': {}}
    model = tf.keras.models.load_model(classification_model_path)
    available_gestures = Gestures(classes_path = available_gestures_path).get_available_gestures()
    detected_gestures = {available_gesture: [] for available_gesture in available_gestures}

    with mp_hands.Hands(model_complexity=model_complexity, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence, max_num_hands=max_num_hands) as hands:
        for time, frame in video.iter_frames(with_times = True):
            frame_keypoints = hands.process(frame)
            if frame_keypoints.multi_hand_landmarks:
                keypoint = [(hand_landmarks, calc_keypoints(frame, hand_landmarks))
                    for hand_landmarks in frame_keypoints.multi_hand_landmarks]
                to_draw['keypoints'][time] = keypoint
                to_draw['classes'][time] = {'class': 'No class', 'conficende': 0}
                predictions = model.predict(np.array(keypoint[-1][-1][:num_features]).reshape(1, num_features))
                predicted_gesture = np.argmax(predictions, axis=1)[0]
                if predictions[0][predicted_gesture] > min_threshold: # minium threshold
                    to_draw['classes'][time]['class'] = available_gestures[predicted_gesture]
                    to_draw['classes'][time]['confidence'] = predictions[0][predicted_gesture] * 100
                    detected_gestures[available_gestures[predicted_gesture]].append(datetime.timedelta(seconds=time)) #try to change this
            else:
                to_draw['keypoints'][time] = []
                to_draw['classes'][time] = None
        if draw_hands:
            def fl(gf, t):
                return draw_keypoints(gf(t), to_draw['keypoints'][t], to_draw['classes'][t])
            video = video.transform(fl, apply_to=['mask'])
        return detected_gestures, video

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Help for hand pose detection.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--video', required=True, help='Path to the video.')
    args = vars(parser.parse_args())
    video = mpy.VideoFileClip(args['video'])
    keypoints = run_detection_hands(video)