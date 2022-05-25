import moviepy.editor as mpy
import tensorflow as tf
import numpy as np
import time, argparse, logging
import datetime
from hand_detection.hand_pose import run_detection_hands
from gestures import Gestures
from actions import *
from hand_detection.model_config import *

def get_gestures(video, fps):
    model = tf.keras.models.load_model('../assets/models/keypoints_classifier.hdf5')
    available_gestures = Gestures(classes_path = '../assets/dataset/labels.csv').get_available_gestures()
    keypoints, video = run_detection_hands(video, draw_hands = True)
    detected_gestures = {available_gesture: [] for available_gesture in available_gestures}
    for frame_idx, frame in enumerate(keypoints): # frame by frame and access first item (normalized coordinates) of the tuple
        if len(frame) == 0:
            continue
        predictions = model.predict(np.array(frame[-1][-1][:num_features]).reshape(1, num_features))
        predicted_gesture = np.argmax(predictions, axis=1)[0]
        if predictions[0][predicted_gesture] > min_threshold: # minium threshold
            detected_gestures[available_gestures[predicted_gesture]].append(datetime.timedelta(seconds=frame_idx/fps))
    return detected_gestures, video
    
def edit_video(args):
    input = args['video']
    extension = input.split('.')[-1]
    output = args['output'] + '.' + extension
    extra_parameters = {}
    video = mpy.VideoFileClip(input)
    if not args['intro'] == None:
        extra_parameters['intro_video'] = mpy.VideoFileClip(args['intro'])

    for action in ['insert_intro', 'cut']:
        # TODO: it  would be more efficent to compute gestures only once, but I don't do that because after cutting video, timestamps would change.
        gestures, video = get_gestures(video, video.fps)
        timestamps = transform_into_timestamps(gestures)
        if not action in timestamps: # if the action has not been detected
            continue
        video = operate_action(action, video, timestamps[action], extra_parameters)

    video.write_videofile(output, threads=args['threads'], remove_temp=True, codec=args['vcodec'], preset=args['compression'], ffmpeg_params=['-crf', args['quality']])
    video.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Help for auto editing software.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--video", required=True, help="Path to the original video.")
    parser.add_argument("-i", "--intro", default=None, help="Path to the intro.")
    parser.add_argument("-o", "--output", default='output', help="Path to the output video.")                             
    parser.add_argument("-c", "--compression", default='medium',  help="Compression value. Possible values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow.")
    parser.add_argument("-q", "--quality", default='24', help="Video quality.")
    parser.add_argument("-vc", "--vcodec", default='libx264', help="Video codec.")
    parser.add_argument("-t", "--threads", default='1', help="Number of threads.")
    parser.add_argument("-d", "--debug", default=False, help="Debug prints.")
    args = vars(parser.parse_args())

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG if args['debug'] else logging.INFO)

    start = time.time()
    edit_video(args)
    end = time.time()
    print(f'Video has been exported in {str(datetime.timedelta(seconds=end-start))}.')