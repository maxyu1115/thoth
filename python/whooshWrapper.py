import os, os.path
import util
from whoosh import index
from whoosh.searching import ResultsPage, Results
from whoosh.fields import *
from whoosh.qparser import QueryParser

import pipeline
import json


BASIC_INDEX = "basic index"
BASIC_SCHEMA = Schema(video_name=TEXT(stored=True), video_path=ID(stored=True), timestamp=NUMERIC(stored=True), content=TEXT(stored=True))

VIDEO_NAME = "video_name"
VIDEO_PATH = "video_path"
TIMESTAMP = "timestamp"
CONTENT = "content"


def initWhoosh(locator: util.DirectoryLocator, index_name: str = BASIC_INDEX, schema: Schema = BASIC_SCHEMA) -> index:
    if not os.path.exists(locator.index_directory):
        os.mkdir(locator.index_directory)

    if index.exists_in(locator.index_directory, indexname=index_name):
        idx = index.open_dir(locator.index_directory, indexname=index_name)
    else:
        idx = index.create_in(locator.index_directory, schema, indexname=index_name)

    return idx


class WhooshWrapper:
    def __init__(self, locator: util.DirectoryLocator, index_name=BASIC_INDEX, schema=BASIC_SCHEMA):
        self.ix: index = initWhoosh(locator, index_name=index_name, schema=schema)

    def searchWhoosh(self, phrase: str, page_num=1, pagelen=10) -> ResultsPage:
        with self.ix.searcher() as searcher:
            query = QueryParser(CONTENT, BASIC_SCHEMA).parse(phrase)
            page_results = searcher.search_page(query, page_num, pagelen=pagelen)
            return page_results.results

    def createIndex(self, video_name: str, video_path: str, timestamp: int,  content: str) -> None:
        writer = self.ix.writer()
        writer.add_document(video_name=video_name, video_path=video_path, timestamp=timestamp,  content=content)
        writer.commit()


class Indexer(pipeline.ProcessingOperation):
    def __init__(self):
        self.whoosh = None
        pass

    def _processListIndex(self, file_locator: util.FileLocator, filenames: list[str]):
        for filename in filenames:
            with open(filename, "r") as read_file:
                slice_data = json.load(read_file)
            assert(slice_data[0] == file_locator.file_pathname)
            slice_data = slice_data[1:]
            for slice in slice_data:
                self.whoosh.createIndex(file_locator.file_name, file_locator.file_pathname, slice[util.START_TIME], slice[util.TEXT])

    def process(self, file_locator: util.FileLocator) -> None:
        self.whoosh = WhooshWrapper(file_locator)
        self._processListIndex(file_locator, [file_locator.getSpeechJsonName(), file_locator.getOCRJsonName()])

