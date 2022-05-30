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
                timestamps.append({'begin': begin.total_seconds(), 'end': end.total_seconds()})
        return timestamps

    def get_insert_intro_timestamps(detected_gestures):
        begin = min(detected_gestures) - seconds_before_and_after_signs
        end = max(detected_gestures) + seconds_before_and_after_signs
        timestamps = [{'begin': begin.total_seconds(), 'end': end.total_seconds()}]
        return timestamps

    timestamps = {}
    for gesture_type in detected_gestures.keys():
        if len(detected_gestures[gesture_type]) == 0:
            continue
        timestamps[gesture_type] = locals()['get_' + gesture_type + '_timestamps'](detected_gestures[gesture_type])
    return timestamps

def operate_action(action, video, timestamps, extra_parameters={}):
    ''' Operate an action on the input video.
    Parameters:
    action (String): name of the action to be performed.
    video (moviepy.editor.VideoFileClip): input video. 
    timestamps (List[Dict[begin, end]]): list of timestamps.
    extra_parameters (Dict[parameter]): dict with extra parameters.

    Returns:
    new_video (moviepy.editor.VideoFileClip): edited video. 
    delta_seconds (Int): when an operation takes place, the whole duration of the clip changes. Thus, previously detected gestures need to adjust their timestamps as well.
    '''

    def insert_intro(video, timestamps, extra_parameters):
        if not 'intro_video' in extra_parameters.keys():
            return video
        timestamps = timestamps[0]
        part_1 = video.subclip(0, timestamps['begin'])
        part_2 = extra_parameters['intro_video']
        part_3 = video.subclip(timestamps['end'], video.duration)
        new_video = mpy.concatenate_videoclips([part_1, part_2, part_3], method='compose')
        return new_video, timestamps['begin'] - timestamps['end'] + extra_parameters['intro_video'].duration

    def cut(video, timestamps, extra_parameters):
        for cut in timestamps:
            new_video = video.cutout(cut['begin'], cut['end'])
        return new_video, cut['begin'] - cut['end']   

    new_video, delta_seconds = locals()[action](video, timestamps, extra_parameters)
    return new_video, delta_seconds