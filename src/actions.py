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
                timestamps.append((begin.total_seconds(), end.total_seconds()))
        return timestamps

    def get_insert_intro_timestamps(detected_gestures):
        begin = min(detected_gestures) - seconds_before_and_after_signs
        end = max(detected_gestures) + seconds_before_and_after_signs
        timestamps = (begin.total_seconds(), end.total_seconds())
        return timestamps

    timestamps = {}
    for gesture_type in detected_gestures.keys():
        if len(detected_gestures[gesture_type]) == 0:
            continue
        timestamps[gesture_type] = eval('get_' + gesture_type + '_timestamps')(detected_gestures[gesture_type])
    return timestamps

def operate_action(action, video, timestamps, extra_parameters={}):
    def calculate_delta_seconds(deleted_seconds, added_seconds):
        """When an operation takes place, the whole duration of the clip changes. Thus, previously detected gestures need to adjust their timestamps as well.
        Parameters:
        deleted_seconds (Dict['begin', 'end']: A dictionary with two keys. Begin and end of a cut.
        added_seconds (List[Int]): Each number represents the duration of an added video.

        Returns:
        delta_seconds (Int): The number of seconds that differ the new video from the old one. 
            A positive number means that the new video is longer than the old one and vice-versa.
        """
        delta_seconds = deleted_seconds['begin'] - deleted_seconds['end']
        for added_second in added_seconds:
            delta_seconds += added_second
        return delta_seconds

    def insert_intro(video, timestamps, extra_parameters):
        if not 'intro_video' in extra_parameters.keys():
            return video
        part_1 = video.subclip(0, timestamps[0])
        part_2 = extra_parameters['intro_video']
        part_3 = video.subclip(timestamps[1], video.duration)
        new_video = mpy.concatenate_videoclips([part_1, part_2, part_3], method="compose")
        return new_video, calculate_delta_seconds({'begin': timestamps[0], 'end': timestamps[1]}, [extra_parameters['intro_video'].duration])

    def cut(video, timestamps, extra_parameters):
        for cut in timestamps:
            video = video.cutout(cut[0] + extra_parameters['delta_timestamps'], cut[1] + extra_parameters['delta_timestamps'])
        return video, calculate_delta_seconds({'begin': cut[0], 'end': cut[1]}, [extra_parameters['delta_timestamps']])

    video, delta_seconds = eval(action)(video, timestamps, extra_parameters)
    return video, delta_seconds