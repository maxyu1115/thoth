import subprocess
from tinytag import TinyTag

command_audio = "ffmpeg -i ../videos/{0} -ab 160k -ac 2 -ar 44100 -vn ../audios/{1}"
command_channel = "ffmpeg -i ../audios/{0} -ac 1 ../audios/{1}"

gcp_link = "gs://hackrice-11/{0}"
bucket_name = "hackrice-11"

# from .mp4 to .flac with single channel
def extract_audio_file(filename):
    name = filename.split('.')[0]
    wav_name = name + "_audio.flac"
    wav_right_name = name + "_right.flac"
    subprocess.call(command_audio.format(filename, wav_name), shell=True)
    subprocess.call(command_channel.format(wav_name, wav_right_name), shell=True)
    return "../audios/" + wav_right_name

# uploads the flac file with single channel to cloud
def upload_to_cloud(filename):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob_name = filename + "blob"
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(filename)

    print(
        "File {} uploaded to {}.".format(
            filename, blob_name
        )
    )
    return blob_name   

# returns an array of tuple containing the word and the staring time
# this word is spoken.
def transcribe_file(gcs_uri, filename):
    """Transcribe the given audio file."""
    from google.cloud import speech

    client = speech.SpeechClient()

    tag = TinyTag.get('../audios/' + filename)
    print("the sample rate is", tag.samplerate)

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=tag.samplerate,
        language_code="en-US",
        enable_word_time_offsets=True,  
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=200)
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
            rtn.append((word, start_time.total_seconds()))
    # print(rtn[20:])
    return rtn

# the entry point for this file.
# video_name should not include path but it should include extension
# should be mp4 file
def get_speech_from_video(video_name):
    audio_name = extract_audio_file(video_name)
    blob_name = upload_to_cloud(audio_name)
    return transcribe_file(gcp_link.format(blob_name), audio_name)

get_speech_from_video("test3.mp4")


