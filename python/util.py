import os

TEXT = "text"
IMAGE_LOC = "image"
START_TIME = "start_time"
END_TIME = "end_time"
IMAGE_TIME = "image_time"


def make_ocr_dict(start_time: int, text: str, image_location: str):
    return {START_TIME: start_time, TEXT: text, IMAGE_LOC: image_location}

def make_transcribe_dict(start_time: int, text: str, image_location: str, end_time):
    return {START_TIME: start_time, TEXT: text, IMAGE_LOC: image_location, END_TIME: end_time}

def make_detect_dict(start_time: int, end_time: int, image_time: int, image_location: str):
    return {START_TIME: start_time, END_TIME: end_time, IMAGE_TIME: image_time, IMAGE_LOC: image_location}


def __make_path_dir__(path_name: str):
    if not os.path.exists(path_name):
        os.makedirs(path_name)


class DirectoryLocator:
    """
    Directory locator utility class
    """

    def __init__(self, output_path: str):
        self.output_path = output_path
        __make_path_dir__(self.output_path)

        self.screenshot_directory = os.path.join(self.output_path, "image")
        __make_path_dir__(self.screenshot_directory)

        self.json_directory = os.path.join(self.output_path, "json")
        __make_path_dir__(self.json_directory)

        self.index_directory = os.path.join(self.output_path, "idx")
        __make_path_dir__(self.index_directory)

        self.audio_directory = os.path.join(self.output_path, "audio")
        __make_path_dir__(self.audio_directory)

    def makeJsonPathname(self, filename: str) -> str:
        return os.path.join(self.json_directory, filename)

    def getScreenshotDirectory(self) -> str:
        """
        Sample output: "xxx/image"
        :return: directory of screenshots
        """
        return self.screenshot_directory

    def getJsonDirectory(self) -> str:
        """
        Sample output: "xxx/json"
        :return: directory of jsons
        """
        return self.json_directory

    def getIndexDirectory(self) -> str:
        """
        Sample output: "xxx/idx"
        :return: directory of search indexes
        """
        return self.index_directory

    def getAudioDirectory(self) -> str:
        """
        Sample output: "xxx/audio"
        :return: directory for audio
        """
        return self.audio_directory


class FileLocator(DirectoryLocator):
    """
    File locator utility class
    """

    def __init__(self, file_pathname: str, output_path: str):
        super().__init__(output_path)
        self.file_pathname = file_pathname
        self.file_name = os.path.basename(file_pathname)
        filename_list = self.file_name.split(".")
        if len(filename_list) != 2:
            raise Exception("Bad file name format! ")
        self.file_prefix = str.format("{}_{}_", filename_list[0], filename_list[1])

        self.detect_json_name = self.makeJsonPathname(self.file_prefix + "detect.json")
        self.speech_json_name = self.makeJsonPathname(self.file_prefix + "speech.json")
        self.ocr_json_name = self.makeJsonPathname(self.file_prefix + "ocr.json")

    def getFilePathName(self) -> str:
        return self.file_pathname

    def getFileName(self) -> str:
        return self.file_name

    def getOutputRoot(self) -> str:
        return self.output_path

    def getFilePrefix(self) -> str:
        return self.file_prefix

    def getScreenshotName(self, time_in_milliseconds: int) -> str:
        """
        Sample output: "xxx/image/test_mp4_1034.png"
        :param time_in_milliseconds: time of screenshot in milliseconds
        :return: name of screenshot at time t
        """
        return os.path.join(self.screenshot_directory, self.file_prefix + str(time_in_milliseconds) + ".png")

    def getDetectJsonName(self) -> str:
        return self.detect_json_name

    def getSpeechJsonName(self) -> str:
        return self.speech_json_name

    def getOCRJsonName(self) -> str:
        return self.ocr_json_name


# file_locator = FileLocator("video.mp4", "/Users/TheWanderingPath/Documents/GitHub/thoth/test")
# print(locator.getScreenshotDirectory())
# print(locator.getOCRJsonName())

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
#
# file = os.path.join(file_locator.output_path, "json/test.json")
#
# with open(file, "w") as write_file:
#     json.dump(["hey", {"this":"that"}], write_file)
#
#
# with open(file, "r") as read_file:
#     print(json.load(read_file))