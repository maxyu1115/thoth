The following libraries are required:

`pip install ffmpeg`

`pip install opencv-python`

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