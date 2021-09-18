# Standard PySceneDetect imports:
import json

from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.frame_timecode_new import FrameTimecode
from scenedetect.stats_manager import StatsManager
from typing import List, Tuple

from customDetector import StdDetector
from scenedetect.detectors import ContentDetector, ThresholdDetector

import cv2

import util
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
        frame_lst, output = self._select_frames(scenes, stats, file_locator, frame_method="middle")
        self.export_frames(file_locator, frame_lst)
        # write data to json file
        with open(file_locator.getDetectJsonName(), "w") as write_file:
            json.dump(output, write_file)

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

    def _select_frames(self, scenes: List[Tuple[FrameTimecode, FrameTimecode]],
                       stats_manager: StatsManager, file_locator: FileLocator, frame_method: str):
        output = [file_locator.file_pathname]
        frame_lst = []
        for s, f in scenes:
            start_time = int(s.get_seconds() * 1000)
            end_time = int(f.get_seconds() * 1000)
            image_frame = self.get_best_frame(s.get_frames(), f.get_frames(), stats_manager, frame_method)
            frame_lst.append(image_frame)

            image_time = int(image_frame * 1000 / s.get_framerate())
            image_path = file_locator.getScreenshotName(image_time)
            output.append(util.make_detect_dict(start_time, end_time, image_time, image_path))

        return frame_lst, output

    @staticmethod
    def export_frames(file_locator: FileLocator, frames: List[int]):
        cap = cv2.VideoCapture(file_locator.file_pathname)

        # Find OpenCV version and then get FPS
        (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')
        if int(major_ver) < 3:
            fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = cap.get(cv2.CAP_PROP_FPS)

        i = 0
        while cap.isOpened() and i < len(frames):
            frame_num = frames[i]
            cap.set(1, frame_num)
            ret, frame = cap.read()
            if not ret:
                break
            out_path = file_locator.getScreenshotName(frame_num * 1000 // fps)
            cv2.imwrite(out_path, frame)
            i += 1

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def get_best_frame(start_frame: int, end_frame: int, states_manager: StatsManager, frame_method="smart"):
        if frame_method == "last":
            return end_frame
        elif frame_method == "first":
            return start_frame
        elif frame_method == "middle":
            return (start_frame + end_frame) // 2
        elif frame_method == "smart":
            return (start_frame + end_frame) // 2


# Testing slideDetect
if __name__ == "__main__":
    filename = "test/SlideChangeTest1.mov"
    locator = FileLocator(filename, "/output3/temp")
    detect = SlideDetect("unanimated_slides")
    detect.process(locator)
