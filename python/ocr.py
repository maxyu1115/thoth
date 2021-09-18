import pytesseract
import cv2
from cv2 import VideoCapture

import util
from util import FileLocator

import glob
import json
import pipeline


def extractText(image_location: str, preprocess: str = "none") -> str:
    # load the example image and convert it to grayscale
    image = cv2.imread(image_location)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove noise
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # apply ocr to extract text
    return pytesseract.image_to_string(gray)


class OCR(pipeline.ProcessingOperation):
    def process(self, video: VideoCapture, file_locator: FileLocator) -> VideoCapture:
        # Don't do anything to the video. Instead read the screenshots and
        filenames = glob.glob(file_locator.getScreenshotDirectory() + "/" + file_locator.getFilePrefix() + "*")
        output_json_name = file_locator.getOCRJsonName()
        output = []
        for filename in filenames:
            text = extractText(filename)
            # parse start time from screenshot file name
            start_time = int((filename.split("_")[-1]).split(".")[0])
            output.append(util.make_ocr_dict(start_time, text, filename))

        # write data to json file
        with open(output_json_name, "w") as write_file:
            json.dump(output, write_file)

        return video

# filename = "/video_mp4_1003.png"
# print(int((filename.split("_")[-1]).split(".")[0]))
#
# file_locator = util.FileLocator("video.mp4", "/Users/TheWanderingPath/Documents/GitHub/thoth/python")
#
# directory_name = file_locator.getScreenshotDirectory() + "/" + file_locator.getFilePrefix()
#
# print(directory_name)
#
# print(glob.glob(directory_name + "*"))
# print(glob.glob("/*"))
