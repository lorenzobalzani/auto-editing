import moviepy.editor as mpy
import time
import argparse

def get_gestures(video):
    # some ops on video
    gestures_timestamp = [('00:00:10.000', '00:00:25.000'),
        ('00:04:00.000', '00:05:00.000')]
    return gestures_timestamp
    
def edit_video(args):
    input = args['video']
    extension = input.split('.')[-1]
    output = args['output'] + '.' + extension

    video = mpy.VideoFileClip(input)
    cuts = get_gestures(video)

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
    args = vars(parser.parse_args())
   

    start = time.time()
    edit_video(args)
    end = time.time()
    print(f'Exporting video has finished in {float((end - start) / 60)} minutes')