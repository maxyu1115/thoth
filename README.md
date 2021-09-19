# Thoth - the video distiller
### Team members: Kaichun Luo, Lorraine Lyu, Victor Song, Max Yu

## Inspiration
With the Pandemic continuously affecting our daily life, online educational videos have become increasingly popular. Be it hybrid or completely asynchronous, many lectures and meetings are pre-recorded or delivered on Zoom with a recording available. Watching and rewatching video lectures can be painstaking and demotivating, given its length and lack of interactions. But what if we can turn a video lecture into beautiful notes with pictures so that we can even search contents in a pile of videos? What if you can search and find which exact lecture you missed talked about a specific topic? That is what we bring to you in this project.

## What it does
- Slices video clips according to contents (for example, slides)
- Transcribes speech for each video slice
- Extracts the most representative image from each video slice
- OCR (Optical Character Recognition) extract text from each image
- Displays slides and transcripts side by side
- Enables content searching in the video through transcribed speech and recognized text from images

## How we built it
### Full-stack web application
- Front-end: We used Material UI and React.js to make requests to the backend and present the output in an accessible manner.
- Back-end: We used Flask in Python to handle http requests from the front-end and run our video processing pipeline.

### Video processing pipeline
- Scene Detection: We utilized the PySceneDetect package as a guideline and on top of that, we designed and implemented a novel customized detector which relies heavily on Numpy and OpenCV.
- Speech Recognition: We used Google Cloud Speech-To-Text API to transcribe the videos.
- OCR: We used Tesseract for OCR on the existing screenshots generated by Scene Detection.
- Search Indexing: We used Whoosh, an open source search engine and variant of Lucene, to index all our text generated by Speech Recognition and OCR.

## Challenges we ran into
It was not an easy project. Initially we wanted to build a native JavaScript program that calls our pipeline written in Python. This did not work out, and we turned to a full-stack web application when we had less than 12 hours left. Miscellaneous bugs came out when we were trying to push everything in such a tight time limit, especially when doing things that we are not familiar with. We spent a lot of time figuring out how to use multi-threading and multi-processing to speed up video processing, and it also took a lot of fine tuning to make sure that our scene detector model fits various videos. Glad that we made it!


# Environment Requirements

The following libraries are required:

`pip install ffmpeg`

`pip install opencv-python`

`pip install scenedetect`

`pip install pyinstaller`

`pip install pillow`

`pip install pytesseract`

To run video_to_text.py (team members only):

1. cd into thoth
2. `mkdir audios & mkdir videos` if you don't have'em
3. `pip3 install tinytag`
4. `pip3 install google-cloud-speech`
5. `pip3 install google-cloud-storage`
6. Log into GCP with your rice email. Generate your credential in Thoth project in GCP (in dashboard left menu IAM & Admin > service accounts > Actions (the dots to the right of the only service account entry)  >Manage Keys > create new key > JSON) 
7. Set up Google auth credential following this section https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable 
8. place .mp4 file or .mov file into vodeos folder and call get_speech_from_video("video name"), the video should be short for testing. It takes some time to transcribe.
