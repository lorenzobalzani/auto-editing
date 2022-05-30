import moviepy.editor as mpy
import tensorflow as tf
import numpy as np
import time, argparse, logging
import datetime
from hand_detection.hand_pose import run_detection_hands
from actions import *
    
def edit_video(args):
    input = args['video']
    extension = input.split('.')[-1]
    output = args['output'] + '.' + extension
    extra_parameters = {'delta_timestamps': 0}
    video = mpy.VideoFileClip(input)
    if not args['intro'] == None:
        extra_parameters['intro_video'] = mpy.VideoFileClip(args['intro'])

    gestures, video = run_detection_hands(video, \
                                        '../assets/models/keypoints_classifier.hdf5', \
                                        '../assets/dataset/labels.csv', \
                                        draw_hands = args['debug'])
    timestamps = transform_into_timestamps(gestures)

    actions = ['insert_intro', 'cut'] if not args['debug'] else []

    for action in actions: # TODO: if they're switched, they won't work
        if not action in timestamps: # if the action has not been detected
            continue
        video, extra_parameters['delta_timestamps'] = operate_action(action, video, timestamps[action], extra_parameters)

    video.write_videofile(output, threads=args['threads'], remove_temp=True, codec=args['vcodec'], preset=args['compression'], ffmpeg_params=['-crf', args['quality']])
    video.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Help for auto editing software.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--video', required=True, help='Path to the original video.')
    parser.add_argument('-i', '--intro', default=None, help='Path to the intro.')
    parser.add_argument('-o', '--output', default='output', help='Path to the output video.')                             
    parser.add_argument('-c', '--compression', default='medium',  help='Compression value. Possible values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow.')
    parser.add_argument('-q', '--quality', default='10', help='Video quality. 51: the worst - 0: the best (lossless).')
    parser.add_argument('-vc', '--vcodec', default='libx264', help='Video codec.')
    parser.add_argument('-t', '--threads', default='1', help='Number of threads.')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Export the whole video w/ printed gestures and classifications.')
    args = vars(parser.parse_args())

    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG if args['debug'] else logging.INFO)

    start = time.time()
    edit_video(args)
    end = time.time()
    print(f'Video has been exported in {str(datetime.timedelta(seconds=end-start))}.')