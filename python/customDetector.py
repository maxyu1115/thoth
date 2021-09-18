from scenedetect.scene_detector import SceneDetector

import numpy as np


class StdDetector(SceneDetector):
    """CustomDetector class to implement a scene detection algorithm."""

    FRAME_SCORE_KEY = 'std_val'
    STD_RED, STD_GREEN, STD_BLUE = ('std_r', 'std_g', 'std_b')
    METRIC_KEYS = [FRAME_SCORE_KEY, STD_RED, STD_GREEN, STD_BLUE]

    def __init__(self, skip: int = 10, window: int = 10, threshold: int = 10, average: int = 1):
        super(StdDetector, self).__init__()
        self.skip = skip
        self.window = window
        self.threshold = threshold
        self.average = average
        self.height, self.width = None, None
        self.last_frames = []
        self.averaged_frames = []
        self.last_scene_cut = None

    def get_metrics(self):
        return StdDetector.METRIC_KEYS

    def is_processing_required(self, frame_num : int):
        return self.stats_manager is None or (
            not self.stats_manager.metrics_exist(frame_num, StdDetector.METRIC_KEYS))

    # Calculate std from a list of frames or averaged frames
    def calculate_std(self, frame_num : int):
        std_mat = np.std(np.stack(self.averaged_frames, axis=-1), axis=-1)
        std_val = np.mean(np.sum((std_mat * std_mat), axis=-1) ** 0.5)
        std_r, std_g, std_b = np.mean(np.mean(std_mat, axis=0), axis=0)

        if self.stats_manager is not None:
            self.stats_manager.set_metrics(frame_num, {
                self.FRAME_SCORE_KEY: std_val, self.STD_RED: std_r,
                self.STD_GREEN: std_g, self.STD_BLUE: std_b})
        # print(type(std_val))
        return std_val

    def process_frame(self, frame_num : int, frame_img : np.ndarray):
        cut_list = []

        # Check whether has been initialized
        if not self.last_frames:
            self.height, self.width = frame_img.shape[:2]

        # Update list of frames
        self.last_frames.append(frame_img)
        avg_frame = np.mean(np.stack(self.last_frames, axis=-1), axis=-1) if self.average > 1 else frame_img
        self.averaged_frames.append(avg_frame)

        # Maintain length of last_frames
        if len(self.last_frames) >= self.average:
            self.last_frames.pop(0)

        # Start computing only when we have a full list of averaged frames
        if len(self.averaged_frames) > self.window:
            self.averaged_frames.pop(0)
        else:
            return cut_list

        # Compute once every "skip" frames
        if frame_num % self.skip != 0:
            return cut_list

        # Start computing std of list of averaged frames
        score = self.calculate_std(frame_num)
        if score > self.threshold:
            if self.last_scene_cut is not None:
                cut_list = [self.last_scene_cut, frame_num]
            self.last_scene_cut = frame_num
        return cut_list

    def post_process(self, scene_list):
        return []
