import argparse
import os
import cv2
import pipeline
import util
import ocr
import video_to_text

parser = argparse.ArgumentParser(description='Run the thoth pipeline. ')
parser.add_argument('--vid', type=str, help='location of the video')
parser.add_argument('--target', type=str, help='location of output folder')

args = parser.parse_args()


def setupPipeline():
    processor = pipeline.Pipeline()
    # TODO: add std detect here

    processor.addOperation(ocr.OCR())
    processor.addOperation(video_to_text.VideoToTextProcessOperation())

    # TODO: add speech2text here
    # TODO: add whoosh indexing here
    return processor


def main():
    # do stuff here
    # with open(os.path.join(args.target, "your_file.txt"), 'w') as f:
    #     f.write("TEST!!!\n")

    # setup pipeline
    processor = setupPipeline()

    locator = util.FileLocator(args.vid, args.target)

    processor.processVideo(locator)
    return


if __name__ == '__main__':
    main()