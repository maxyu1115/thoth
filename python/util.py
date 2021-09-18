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
    def __init__(self, file_name: str, output_path: str):
        self.file_name = file_name
        filename_list = file_name.split(".")
        if len(filename_list) != 2:
            raise Exception("Bad file name format! ")
        self.file_prefix = str.format("{}_{}_", filename_list[0], filename_list[1])
        self.output_path = output_path if output_path[-1] == '/' else output_path + "/"

        self.screenshot_directory = self.output_path + "image"

        self.json_directory = self.output_path + "json"
        self.speech_json_name = str.format("{}/{}speech.json", self.getJsonDirectory(), self.file_prefix)
        self.ocr_json_name = str.format("{}/{}ocr.json", self.getJsonDirectory(), self.file_prefix)

        self.index_directory = self.output_path + "idx"

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
        return str.format("{}/{}{}.png", self.screenshot_directory, self.file_prefix, time_in_seconds)

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