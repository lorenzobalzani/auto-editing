import datetime

def transform_into_timestamps(detected_gestures):
    seconds_before_and_after_signs = datetime.timedelta(seconds=1)
    threshold = datetime.timedelta(seconds=5)

    def get_cut_timestamps(detected_gestures):
        groups = []
        for timestamp in detected_gestures:
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
        for cut in timestamps:
            video = video.cutout(cut[0], cut[1])
        return video

    return eval(action)(video, timestamps, extra_parameters)