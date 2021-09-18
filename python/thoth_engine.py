import argparse
import pipeline
import util
import slideDetect
import ocr
import video_to_text
import whooshWrapper

import thothSearchServer

parser = argparse.ArgumentParser(description='Run the thoth pipeline. ')
parser.add_argument('-s', action="store_true", help='run server')
parser.add_argument('--port', type=int, default=8080, help='run server on specified port, default 8080')
parser.add_argument('--vid', type=str, help='location of the video')
parser.add_argument('--animated', type=bool, help='whether slides are animated or not')
parser.add_argument('--target', type=str, help='location of output folder')

args = parser.parse_args()


def setupPipeline():
    processor = pipeline.Pipeline()
    processor.addOperation(slideDetect.SlideDetect("animated_slides" if args.animated else "unanimated_slides"))
    processor.addOperation(video_to_text.VideoToTextProcessOperation())
    processor.addOperation(ocr.OCR())
    processor.addOperation(whooshWrapper.Indexer())
    return processor


def main():
    if args.s:
        thothSearchServer.startServer(args.target, args.port)
    else:
        # setup pipeline
        processor = setupPipeline()

        locator = util.FileLocator(args.vid, args.target)

        processor.processVideo(locator)
    return


if __name__ == '__main__':
    main()