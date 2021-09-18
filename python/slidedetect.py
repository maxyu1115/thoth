from scenedetect import VideoManager
# Standard PySceneDetect imports:
from scenedetect import VideoManager
from scenedetect import SceneManager

# For content-aware scene detection:
from scenedetect.detectors import ContentDetector


from scenedetect.scene_detector import SceneDetector
import numpy as np

sd = []


class CustomDetector(SceneDetector):
    """CustomDetector class to implement a scene detection algorithm."""
    def __init__(self):
        self.height = 50
        self.width = 50
        self.pointDist = 3
        self.history = [ [ [] for i in range(self.width) ] for j in range(self.height) ]
        self.frameFilter = 60
        pass


    def process_frame(self, frame_num, frame_img):
        if frame_num % self.frameFilter != 0:
            return []
        s = 0
        for i in range(0, self.width):
            for j in range(0, self.height):
                rgb = frame_img[i * self.pointDist][j * self.pointDist]
                self.history[i][j].append(rgb[0] + rgb[1] + rgb[2])
                if frame_num > 10 * self.frameFilter:
                    # print(self.history[i][j][(frame_num // 30) - 10:])
                    s += np.std(self.history[i][j][(frame_num // self.frameFilter) - 10:])
        # print(frame_img[0])
        sd.append(s)
        return []

    def post_process(self, scene_list):
        return []


def find_scenes(video_path, threshold=30.0):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        CustomDetector())

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    # Each returned scene is a tuple of the (start, end) timecode.
    return scene_manager.get_scene_list()

scenes = find_scenes('video.mp4')

with open('your_file.txt', 'w') as f:
    for item in sd:
        f.write("%s\n" % item)

import matplotlib.pyplot as plt

plt.plot(range(0, len(sd)),sd)
plt.title('title name')
plt.xlabel('xAxis name')
plt.ylabel('yAxis name')
plt.show()
