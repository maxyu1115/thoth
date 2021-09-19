import subprocess
from multiprocessing import Pool

import util
from util import bcolors
import json
from pipeline import ProcessingOperation
from tinytag import TinyTag
from google.cloud import storage
from google.cloud import speech
import os
import glob

command_audio = "ffmpeg -i {0} -ab 160k -ac 2 -ar 16000 -vn {1}"
command_channel = "ffmpeg -i {0} -ac 1 {1}"
json_convert_progress = "filename: {0} \n text : {1} \n start_time : {2} \n end_time : {3}"

gcp_link = "gs://hackrice-11/{0}"
bucket_name = "hackrice-11"


# from .mp4 to .flac with single channel
class VideoToTextTranscriber(ProcessingOperation):
    """
    Extracts the audio, then calls GCP to transcribe the speech to text asynchronously
    """

    def __init__(self) -> None:
        super().__init__()
        self.file_locator = None
        self.word_list = []

    def process(self, file_locator: util.FileLocator, context: dict) -> None:
        self.file_locator = file_locator
        context["word_lst"] = Pool().apply_async(self.get_speech_from_video, args=())
        # context["word_lst"] = self.get_speech_from_video()
        # self.assemble_words_by_slides(word_list)

    def postProcess(self, file) -> None:
        audio_dir = self.file_locator.getAudioDirectory()
        files = glob.glob(audio_dir + "/*")
        for f in files: 
            print(f"{bcolors.OKBLUE}removing files{bcolors.ENDC}", f)
            os.remove(f)

    def extract_audio_file(self, filename):
        name = self.file_locator.getFileName().split('.')[0]
        flac_name = self.file_locator.getAudioDirectory() + "/" + name + "_audio.flac"
        flac_right_name = self.file_locator.getAudioDirectory() + "/" + name + "_right.flac"
        subprocess.call(command_audio.format(filename, flac_name), shell=True)
        subprocess.call(command_channel.format(flac_name, flac_right_name), shell=True)
        return flac_right_name

    # uploads the flac file with single channel to cloud
    def upload_to_cloud(self, filename):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob_name = self.file_locator.getFileName() + "-blob"
        blob = bucket.blob(blob_name)

        blob.upload_from_filename(filename)

        print(
            (bcolors.OKBLUE + "File {} uploaded to {}." + bcolors.ENDC).format(
                filename, blob_name
            )
        )
        return blob_name   

    # returns an array of tuple containing the word and the staring time
    # this word is spoken.
    def transcribe_file(self, gcs_uri, filename):
        """Transcribe the given audio file."""
        client = speech.SpeechClient()

        tag = TinyTag.get(filename)
        # print("the sample rate is", tag.samplerate)

        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=tag.samplerate,
            language_code="en-US",
            enable_word_time_offsets=True,  
            enable_automatic_punctuation=True,
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print(f"{bcolors.OKBLUE}Waiting for operation to complete...{bcolors.ENDC}")
        response = operation.result(timeout=3000)
        rtn = []

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            alternative = result.alternatives[0]
            print(u"Transcript: {}".format(result.alternatives[0].transcript))
            print("Confidence: {}".format(result.alternatives[0].confidence))

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                rtn.append((word, start_time.total_seconds() * 1000, end_time.total_seconds() * 1000))
        # print(rtn[20:])
        self.word_list = rtn
        return rtn

    # the entry point for this file.
    # should be mp4 or mov file
    def get_speech_from_video(self):
        audio_name = self.extract_audio_file(self.file_locator.getFilePathName())
        blob_name = self.upload_to_cloud(audio_name)
        return self.transcribe_file(gcp_link.format(blob_name), audio_name)


class VideoToTextAssembler(ProcessingOperation):
    """
    Waits for GCP to transcribe the speech to text, and assemble to output
    """

    def process(self, file_locator: util.FileLocator, context: dict) -> None:
        # wait on the async task
        word_lst = context["word_lst"].get()
        # word_lst = context["word_lst"]
        return self.assemble_words_by_slides(file_locator, word_lst)

    def postProcess(self, file_locator: util.FileLocator) -> None:
        util.cleanDir(file_locator.getAudioDirectory())

    @staticmethod
    def assemble_words_by_slides(file_locator: util.FileLocator, word_list):
        detect_json_path = file_locator.getDetectJsonPathName()
        # Opening JSON file
        jfile = open(detect_json_path,)
        
        # returns JSON object as
        # a dictionary
        slides = json.load(jfile)
        str = ""
        idx = 0
        output = [file_locator.getFileName()]
        output_json_name = file_locator.getSpeechJsonPathName()

        # print("word list", word_list[:20])
        # print("json time", output)

        for i in range(1, len(slides)):
            slide = slides[i]
            start_time = slide["start_time"]
            end_time = slide["end_time"]
            file_name = file_locator.getScreenshotName(start_time)
            str = ""
            while idx < len(word_list):
                # print("start time", start_time)
                # print("end time", end_time)
                # print("word start time ", word_list[idx][1])
                # print("word end time ", word_list[idx][2])
                if word_list[idx][2] <= end_time:
                    str += " " + word_list[idx][0]
                    idx += 1
                else: 
                    output.append(util.make_transcribe_dict(start_time, str, file_name, end_time))
                    print(json_convert_progress.format(file_name, str, start_time, end_time))
                    break
            if len(output) == 1 or output[-1]["end_time"] != end_time:
                output.append(util.make_transcribe_dict(start_time, str, file_name, end_time))

        
        # write data to json file
        with open(output_json_name, "w") as write_file:
            json.dump(output, write_file)

