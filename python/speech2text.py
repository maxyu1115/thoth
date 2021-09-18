import pipeline
from cv2 import VideoCapture


class SpeechToTextProcessing(pipeline.ProcessingOperation):

    def process(self, video: VideoCapture) -> VideoCapture:
        return video