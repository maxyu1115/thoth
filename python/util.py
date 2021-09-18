class FileLocator:
    """
    File locator utility class
    """
    def __init__(self, file_name: str, output_path: str):
        self.file_name = file_name
        lst = file_name.split(".")
        if len(lst) != 2:
            raise Exception("Bad file name format! ")
        self.name = lst[0]
        self.extension = lst[1]
        self.output_path = output_path if output_path[-1] == '/' else output_path + "/"

    def getOutputRoot(self) -> str:
        return self.output_path

    def getScreenshotDirectory(self) -> str:
        """
        Sample output: "xxx/image"
        :return: directory of screenshots
        """
        return self.output_path + "image"

    def getJsonDirectory(self) -> str:
        """
        Sample output: "xxx/json"
        :return: directory of jsons
        """
        return self.output_path + "json"

    def getSpeechJsonName(self) -> str:
        return str.format("{}/{}_{}_speech.json", self.getJsonDirectory(), self.name, self.extension)

    def getOCRJsonName(self) -> str:
        return str.format("{}/{}_{}_ocr.json", self.getJsonDirectory(), self.name, self.extension)

    def getIndexDirectory(self) -> str:
        """
        Sample output: "xxx/idx"
        :return: directory of search indexes
        """
        return self.output_path + "idx"


# locator = FileLocator("output.txt", "output/temp")
# print(locator.getScreenshotDirectory())
# print(locator.getOCRJsonName())
