import cv2
from cv2 import VideoCapture
import util

class ProcessingOperation:
    """
    Interface for all video processing algorithms we add to our pipeline
    """
    def process(self, video: VideoCapture, file_locator: util.FileLocator) -> VideoCapture:
        """
        :param video: video that we want to process
        :param file_locator: file locator to locate files and directories
        :return: video after processing
        """
        raise NotImplementedError()

    def postProcess(self) -> None:
        """
        Post processing hook for algorithms that want to do things after the pipeline finishes
        :return: void return
        """
        pass


class Pipeline:
    """
    Video processing pipeline
    """
    def __init__(self):
        self.operations: list[ProcessingOperation] = []

    def addOperation(self, op: ProcessingOperation):
        self.operations.append(op)

    def processVideo(self, video: VideoCapture, file_locator: util.FileLocator) -> VideoCapture:
        for op in self.operations:
            video = op.process(video, file_locator)

        for op in self.operations:
            op.postProcess()

        return video


