import os

TEXT = "text"
IMAGE_LOC = "image"
START_TIME = "start_time"
END_TIME = "end_time"


def make_ocr_dict(start_time: int, text: str, image_location: str):
    return {START_TIME: start_time, TEXT: text, IMAGE_LOC: image_location}


class FileLocator:
    """
    File locator utility class
    """
    def __init__(self, file_pathname: str, output_path: str):
        self.file_pathname = file_pathname
        self.file_name = os.path.basename(file_pathname)
        filename_list = self.file_name.split(".")
        if len(filename_list) != 2:
            raise Exception("Bad file name format! ")
        self.file_prefix = str.format("{}_{}_", filename_list[0], filename_list[1])
        self.output_path = output_path

        self.screenshot_directory = os.path.join(self.output_path, "image")

        self.json_directory = os.path.join(self.output_path, "json")
        self.speech_json_name = os.path.join(self.json_directory, self.file_prefix + "speech.json")
        self.ocr_json_name = os.path.join(self.json_directory, self.file_prefix + "ocr.json")

        self.index_directory = os.path.join(self.output_path, "idx")

    def getFilePathName(self) -> str:
        return self.file_pathname

    def getFileName(self) -> str:
        return self.file_name

    def getOutputRoot(self) -> str:
        return self.output_path

    def getFilePrefix(self) -> str:
        return self.file_prefix

    def getScreenshotDirectory(self) -> str:
        """
        Sample output: "xxx/image"
        :return: directory of screenshots
        """
        return self.screenshot_directory

    def getScreenshotName(self, time_in_seconds: int) -> str:
        """
        Sample output: "xxx/image/test_mp4_1034.png"
        :param time_in_seconds: time of screenshot in seconds
        :return: name of screenshot at time t
        """
        return os.path.join(self.screenshot_directory, self.file_prefix + str(time_in_seconds) + ".png")

    def getJsonDirectory(self) -> str:
        """
        Sample output: "xxx/json"
        :return: directory of jsons
        """
        return self.json_directory

    def getSpeechJsonName(self) -> str:
        return self.speech_json_name

    def getOCRJsonName(self) -> str:
        return self.ocr_json_name

    def getIndexDirectory(self) -> str:
        """
        Sample output: "xxx/idx"
        :return: directory of search indexes
        """
        return self.index_directory


# locator = FileLocator("output.txt", "output/temp")
# print(locator.getScreenshotDirectory())
# print(locator.getOCRJsonName())

#
#
# class OCRJson:
#     def __init__(self):
#         self.start_time = 10
#         self.text = ""
#         self.image_location = ""
#
# test = OCRJson()
# test.image_location = "temp"
# import json
# temp = json.dumps(test.__dict__)
#
# print(json.dumps([2,1,"hey"]))
#
# print(temp)
#
#
#
# print(json.loads(temp))