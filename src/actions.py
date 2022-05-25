import datetime
import moviepy.editor as mpy
from config import *

def transform_into_timestamps(detected_gestures):
    seconds_before_and_after_signs = datetime.timedelta(seconds=seconds_difference_before_and_after_signs)
    threshold = datetime.timedelta(seconds=min_seconds_between_two_signs)

    def get_cut_timestamps(detected_gestures):
        groups = []
        timestamps = []
        for timestamp in detected_gestures:
            if not groups or timestamp - group[0] > threshold:
                group = []
                groups.append(group)
            group.append(timestamp)
        if not len(groups) % 2 == 0:
            print(f'Error! Number of cut sign detected is not even: {len(groups)}.')
            return timestamps
        for idx, group in enumerate(groups):
            if idx % 2 == 0:
                begin = group[0] - seconds_before_and_after_signs
            else:
                end = group[-1] + seconds_before_and_after_signs
                timestamps.append((str(begin), str(end)))
        return timestamps

    def get_insert_intro_timestamps(detected_gestures):
        begin = min(detected_gestures) - seconds_before_and_after_signs
        end = max(detected_gestures) + seconds_before_and_after_signs
        timestamps = (str(begin), str(end))
        return timestamps

    timestamps = {}
    for gesture_type in detected_gestures.keys():
        if len(detected_gestures[gesture_type]) == 0:
            continue
        timestamps[gesture_type] = eval('get_' + gesture_type + '_timestamps')(detected_gestures[gesture_type])
    return timestamps

def operate_action(action, video, timestamps, extra_parameters={}):
    def cut(video, timestamps, extra_parameters):
        for cut in timestamps:
            video = video.cutout(cut[0], cut[1])
        return video

    def insert_intro(video, timestamps, extra_parameters):
        if not 'intro_video' in extra_parameters.keys():
            return video
        return mpy.concatenate_videoclips([video.subclip(0, timestamps[0]), extra_parameters['intro_video'], video.subclip(timestamps[1], video.duration)], method="compose")

    return eval(action)(video, timestamps, extra_parameters)