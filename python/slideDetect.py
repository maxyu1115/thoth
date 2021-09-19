# Standard PySceneDetect imports:
import json

from scenedetect import VideoManager, FrameTimecode
from scenedetect import SceneManager
from scenedetect.stats_manager import StatsManager
from typing import List, Tuple

from customDetector import StdDetector
from scenedetect.detectors import ContentDetector, ThresholdDetector

import numpy as np
import cv2

import util
from util import FileLocator
import pipeline


class SlideDetect(pipeline.ProcessingOperation):

    def __init__(self, video_type):
        assert video_type in ["animated_slides", "unanimated_slides"]
        super(SlideDetect, self).__init__()
        if video_type == "animated_slides":
            self.detector = StdDetector(skip=50, window=10, threshold=10, average=20)
        elif video_type == "unanimated_slides":
            self.detector = ContentDetector(threshold=4, luma_only=True)

    def set_detector(self, new_detector):
        self.detector = new_detector

    def process(self, file_locator: FileLocator, context: dict) -> None:
        print("Processing video: ", file_locator.getFilePathName())
        scenes, stats = self._find_scenes(file_locator.getFilePathName())
        # frame_lst, output = self._select_frames(scenes, stats, file_locator, frame_method="middle")

        frame_lst = [x[1].get_frames() for x in scenes]
        # print(frame_lst)
        output = self.export_frames(file_locator, frame_lst)
        # write data to json file
        with open(file_locator.getDetectJsonPathName(), "w") as write_file:
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

    @staticmethod
    def export_frames(file_locator: FileLocator, frames: List[int]):
        print("Start exporting images...")
        cap = cv2.VideoCapture(file_locator.file_pathname)

        # Find OpenCV version and then get FPS
        (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')
        if int(major_ver) < 3:
            fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = cap.get(cv2.CAP_PROP_FPS)

        print("fps: ", fps)
        output = []
        frame_num = 0
        slice_num = 0
        is_first = True
        while cap.isOpened() and slice_num < len(frames):
            ret, frame = cap.read()
            if not ret:
                break

            if is_first:
                top_frame = frame
                top_frame_idx = frame_num
                top_frame_count = 1
                curr_frame = frame
                curr_frame_count = 1
                is_first = False

            if frame_num == frames[slice_num]:
                # print(frame_num, top_frame_count)
                # End of a video slice
                start_time = int(frames[slice_num - 1] * 1000 / fps) if slice_num > 0 else 0
                end_time = int(frame_num * 1000 / fps)
                image_time = int(top_frame_idx * 1000 / fps)
                image_path = file_locator.getScreenshotPathName(start_time)
                # print(image_path, top_frame)
                cv2.imwrite(image_path, top_frame)
                output.append(util.make_detect_dict(start_time, end_time, image_time, image_path))
                slice_num += 1
                top_frame_count = 1
                top_frame = frame
                top_frame_idx = frame_num
                curr_frame_count = 1
                curr_frame = frame

            if np.sum(1 - np.equal(frame, curr_frame)) < (frame.size * 0.15):
                curr_frame_count += 1
            else:
                if curr_frame_count >= top_frame_count:
                    top_frame = curr_frame
                    top_frame_count = curr_frame_count
                    top_frame_idx = frame_num - curr_frame_count + 1
                curr_frame = frame
                curr_frame_count = 1

            frame_num += 1

        start_time = int(frames[slice_num - 1] * 1000 / fps) if slice_num > 0 else 0
        end_time = int(frame_num * 1000 / fps)
        image_time = int(top_frame_idx * 1000 / fps)
        image_path = file_locator.getScreenshotPathName(start_time)
        # print(image_path, top_frame)
        cv2.imwrite(image_path, top_frame)
        output.append(util.make_detect_dict(start_time, end_time, image_time, image_path))

        cap.release()
        cv2.destroyAllWindows()

        return output


# Testing slideDetect
import os

if __name__ == "__main__":
    filename = "test/SlideChangeTest4.mp4"
    locator = FileLocator(filename, os.getcwd() + "/output4s/temp")
    detect = SlideDetect("unanimated_slides")
    detect.process(locator, dict())
