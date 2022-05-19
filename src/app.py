import moviepy.editor as mpy
import tensorflow as tf
import numpy as np
import time, argparse, logging, pdb, traceback
import datetime
from hand_pose import run_detection_hands, draw_keypoints

num_features = 42
min_threshold = 0.5
seconds_before_and_after_signs = datetime.timedelta(seconds=1)

def get_cutoff_timestamps(gestures_detected):
    threshold = datetime.timedelta(seconds=5)
    groups = []
    for timestamp in gestures_detected:
        if not groups or timestamp - group[0] > threshold:
             group = []
             groups.append(group)
        group.append(timestamp)
    if not len(groups) % 2 == 0:
        print('Error!')
    timestamps = []
    for idx, group in enumerate(groups):
        if idx % 2 == 0:
            begin = group[0] - seconds_before_and_after_signs
        else:
            end = group[-1] + seconds_before_and_after_signs
            timestamps.append((str(begin), str(end)))
    return timestamps

def get_gestures(video, fps):
    model = tf.keras.models.load_model('../assets/models/keypoints_classifier.hdf5')
    keypoints = run_detection_hands(video)
    gestures_detected = []
    for frame_idx, frame in enumerate(keypoints): # frame by frame and access first item (normalized coordinates) of the tuple
        if len(frame) > 0:
            x = np.array(frame[-1][-1][:num_features]).reshape(1, num_features) # 42 is number of features
            predictions = model.predict(x)
            predicted_class = np.argmax(predictions, axis=1)
            if predictions[-1][predicted_class] > min_threshold: # minium threshold
                gestures_detected.append(datetime.timedelta(seconds=(frame_idx/fps)))
    return get_cutoff_timestamps(gestures_detected)
    
def edit_video(args):
    input = args['video']
    extension = input.split('.')[-1]
    output = args['output'] + '.' + extension

    video = mpy.VideoFileClip(input)
    cuts = get_gestures(video, args['fps'])
    video = draw_keypoints(video, run_detection_hands(video), args['fps']) # COULD DELETE

    # cut file
    for cut in cuts:
        video = video.cutout(cut[0], cut[1])

    # save file
    video.write_videofile(output, threads=args['threads'], fps=args['fps'], codec=args['vcodec'], 
        preset=args['compression'], ffmpeg_params=['-crf', args['quality']])
    video.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Help for auto editing software.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--video", required=True, help="Path to the original video.")
    parser.add_argument("-o", "--output", default='output', help="Path to the output video.")                             
    parser.add_argument("-c", "--compression", default='medium',  help="Compression value. Possible values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow.")
    parser.add_argument("-q", "--quality", default='24', help="Video quality.")
    parser.add_argument("-fps", "--fps", default=24, help="Frame per second.")
    parser.add_argument("-vc", "--vcodec", default='libx264', help="Video codec.")
    parser.add_argument("-t", "--threads", default='1', help="Number of threads.")
    parser.add_argument("-d", "--debug", default=False, help="Debug prints.")
    args = vars(parser.parse_args())

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG if args['debug'] else logging.INFO)

    start = time.time()
    edit_video(args)
    end = time.time()
    print(f'Exporting video has finished in {float((end - start) / 60)} minutes')