import sys
import util
import video_to_text

def test_transcribe(locator):
    process = video_to_text.VideoToTextProcessOperation()
    process.setLocator(locator)
    process.get_speech_from_video(locator.getFilePathName())

def test_postprocess_transcribe(locator):
    process = video_to_text.VideoToTextProcessOperation()
    process.setLocator(locator)
    process.postProcess()
    

if __name__ == "__main__":
    if sys.argv[1] == "transcribe":
        filename = sys.argv[2]
        locator = util.FileLocator(filename, "/Users/yunlyu/Desktop/thoth/")
        test_transcribe(locator)
    if sys.argv[1] == "remove":
        filename = sys.argv[2]
        locator = util.FileLocator(filename, "/Users/yunlyu/Desktop/thoth/")
        test_postprocess_transcribe(locator)