# Standard PySceneDetect imports:
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.stats_manager import StatsManager
from typing import List

from customDetector import StdDetector
from scenedetect.detectors import ContentDetector, ThresholdDetector

import cv2

from util import FileLocator
import pipeline


class SlideDetect(pipeline.ProcessingOperation):

    def __init__(self, video_type):
        assert video_type in ["animated_slides", "unanimated_slides"]
        super(SlideDetect, self).__init__()
        if video_type == "animated_slides":
            self.detector = StdDetector(skip=10, window=10, threshold=10, average=1)
        elif video_type == "unanimated_slides":
            self.detector = ContentDetector(threshold=10)

    def set_detector(self, new_detector):
        self.detector = new_detector

    def process(self, file_locator: FileLocator):
        print("Processing video: ", file_locator.file_pathname)
        scenes, stats = self._find_scenes(file_locator.file_pathname)
        frame_lst = self.select_frames(scenes, stats, frame_method="middle")
        return self.export_frames(file_locator, frame_lst)

    def _find_scenes(self, video_path):
        # Create our video & scene managers, then add the detector.
        video_manager = VideoManager([video_path])
        stats_manager = StatsManager()
        scene_manager = SceneManager(stats_manager)
        scene_manager.add_detector(self.detector)

        # Improve processing speed by downscaling before processing.
        video_manager.set_downscale_factor()

        # Start the video manager and perform the scene detection.
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)

        # Each returned scene is a tuple of the (start, end) timecode.
        return scene_manager.get_scene_list(), stats_manager

    @staticmethod
    def select_frames(scenes, stats_manager: StatsManager, frame_method: str):
        # Decides which frame in a scene to extract
        if frame_method == "last":
            return [x[1].get_frames() - 1 for x in scenes]
        elif frame_method == "first":
            return [x[0].get_frames() for x in scenes]
        elif frame_method == "middle":
            return [(x[0].get_frames() + x[1].get_frames()) // 2 for x in scenes]
        elif frame_method == "smart":
            return []
        return []

    @staticmethod
    def export_frames(file_locater: FileLocator, frames: List[int]):
        cap = cv2.VideoCapture(file_locater.file_pathname)

        # Find OpenCV version and then get FPS
        (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')
        if int(major_ver) < 3:
            fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = cap.get(cv2.CAP_PROP_FPS)

        i = 0
        while cap.isOpened() and i < len(frames):
            j = frames[i]
            cap.set(1, j)
            ret, frame = cap.read()
            if not ret:
                break
            out_path = file_locater.getScreenshotName(j * 1000 // fps)
            cv2.imwrite(out_path, frame)
            i += 1

        cap.release()
        cv2.destroyAllWindows()


# Testing slideDetect
if __name__ == "__main__":
    filename = "test/SlideChangeTest1.mov"
    locator = FileLocator(filename, "/output2/temp")
    detect = SlideDetect("unanimated_slides")
    detect.process(locator)
