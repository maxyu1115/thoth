import util
from multiprocessing import Pool


class ProcessingOperation:
    """
    Interface for all video processing algorithms we add to our pipeline
    """
    def process(self, file_locator: util.FileLocator) -> None:
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

    def processVideo(self, file_locator: util.FileLocator) -> None:
        # pool = Pool()

        # # Bad coding style !!!
        # detector = self.operations[0]
        # transcriber = self.operations[1]
        # ocr_helper = self.operations[2]
        # woosh_wraper = self.operations[3]
        # # Action block 1: run video slide detect and transcribe in parallel
        # result = pool.apply_async(transcriber.process, args=(file_locator,))
        # detector.process(file_locator)
        
        # # Action block 2: group words by video slide detection result & OCR
        # ocr_helper.process(file_locator)
        # # print("async result", result.get(timeout = 3000))
        # transcriber.setLocator(file_locator)
        # transcriber.assemble_words_by_slides(result.get())

        # # Action block 3: do indexing for elastic search
        # woosh_wraper.process(file_locator)
        for op in self.operations:
            op.process(file_locator)

        for op in self.operations:
            op.postProcess()

        return


