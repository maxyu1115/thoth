from util import cleanDir, FileLocator
from multiprocessing import Pool


class ProcessingOperation:
    """
    Interface for all video processing algorithms we add to our pipeline
    """
    def process(self, file_locator: FileLocator) -> None:
        """
        :param file_locator: file locator to locate files and directories
        :return: void return
        """
        raise NotImplementedError()

    def postProcess(self) -> None:
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

    def addOperation(self, op: ProcessingOperation):
        self.operations.append(op)

    def processVideo(self, file_locator: FileLocator) -> None:
        pool = Pool()

        # Bad coding style !!!
        detector = self.operations[0]
        transcriber = self.operations[1]
        ocr_helper = self.operations[2]
        woosh_wraper = self.operations[3]
        # Action block 1: run video slide detect and transcribe in parallel
        # OCR starts after detect
        result = pool.apply_async(transcriber.process, args=(file_locator,))
        detector.process(file_locator)
        ocr_helper.process(file_locator)

        # Action block 2: group words by video slide detection result & OCR
        transcriber.setLocator(file_locator)
        transcriber.assemble_words_by_slides(result.get())

        # Action block 3: do indexing for elastic search
        woosh_wraper.process(file_locator)
        # for op in self.operations:
        #     op.process(file_locator)

        self.clean_up(file_locator)

        return

    def clean_up(self, file_locator: FileLocator) -> None:
        ###
        # Cleans up all temporary directoraries.
        ###
        dirs = [file_locator.getAudioDirectory(), file_locator.getJsonDirectory(),
        file_locator.getIndexDirectory(), file_locator.getScreenshotDirectory()]

        [cleanDir(d) for d in dirs]        


