import cv2
from cv2 import VideoCapture

class ProcessingOperation:
    """
    Interface for all video processing algorithms we add to our pipeline
    """
    def process(self, video) -> VideoCapture:
        """
        :param video: video that we want to process
        :return: video after processing
        """
        raise NotImplementedError()

    def postProcess(self) -> None:
        """
        Post processing hook for algorithms that want to do things after the pipeline finishes
        :return:
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

    def processVideo(self, video: VideoCapture) -> VideoCapture:
        for op in self.operations:
            video = op.process(video)

        for op in self.operations:
            op.postProcess()

        return video


