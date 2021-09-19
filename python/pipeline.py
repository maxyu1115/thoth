from util import cleanDir, FileLocator


class ProcessingOperation:
    """
    Interface for all video processing algorithms we add to our pipeline
    """
    def process(self, file_locator: FileLocator, context: dict) -> None:
        """
        :param file_locator: file locator to locate files and directories
        :param context: processing context variables
        :return: void return
        """
        raise NotImplementedError()

    def postProcess(self, file_locator: FileLocator) -> None:
        """
        Post processing hook for algorithms that want to do things after the pipeline finishes
        :return: void return
        """
        return


class Pipeline:
    """
    Video processing pipeline
    """
    def __init__(self):
        self.operations: list[ProcessingOperation] = []
        self.context: dict = dict()
        self.status = 0

    def getProgress(self) -> (int, int):
        return self.status, len(self.operations)

    def addOperation(self, op: ProcessingOperation):
        self.operations.append(op)

    def processVideo(self, file_locator: FileLocator) -> None:
        self.status = 0
        for op in self.operations:
            op.process(file_locator, self.context)
            self.status += 1

        for op in self.operations:
            op.postProcess(file_locator)

        # self.clean_up(file_locator)

        return

    # def clean_up(self, file_locator: FileLocator) -> None:
    #     ###
    #     # Cleans up all temporary directoraries.
    #     ###
    #     dirs = [file_locator.getAudioDirectory(), file_locator.getJsonDirectory(),
    #     file_locator.getIndexDirectory(), file_locator.getScreenshotDirectory()]
    #
    #     [cleanDir(d) for d in dirs]


