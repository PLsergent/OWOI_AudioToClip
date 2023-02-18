# OWOI_AudioToClip
Python module used for the school project OWOI (One Word One Image)

## Installation

After git cloning the repository, you can install the dependencies with the following command:

```bash
poetry install
```

## Credentials

Please provide your credentials in the following environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
export GOOGLE_IMAGES_SEARCH_TOKEN="token"
export GOOGLE_SEARCH_ID="id"
```

## Classes

### TranscriptFactory

This class is used to create a transcript from a text file. It will create a list of words and a list of timestamps.

```python	
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory

transcript_factory = TranscriptFactory(gcs_uri="gs://bucket/file.mp3")
```

Methods:
- ***transcribe_audio_to_text() -> list[dict]***: transcribe audio to text from the gcs_uri and returns a list of dict with the following keys: "word", "start_time" and "end_time"
- ***get_word_timestamps() -> list[dict]***: returns a list of dict with the following keys: "word", "start_time" and "end_time"

This Class should be used to create a transcript from a text file before creating a clip with the ClipMakerFactory.

### ClipMakerFactory

This class is used to create a clip from a transcript.

```python
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory

clip_maker_factory = ClipMakerFactory(video_name, username, transcript, gcs_bucket_name, local_storage_path, gcs_audio_name, with_subtitles=True)
```

Params:
- ***video_name***:str -> name of the video
- ***username***:str -> name of the user
- ***transcript***:list[WordTimestamp] -> list of WordTimestamp
- ***gcs_bucket_dest***:str -> name of the gcs bucket destination
- ***local_storage***:str -> path to the local storage destination
- ***gcs_audio_path***:str -> path to the audio file in the gcs bucket
- ***with_subtitles***:bool -> if True, subtitles will be added to the video

Methods:
- ***clip_maker(word_timestamps: list[WordTimestamp]) -> VideoFileClip***: creates a clip from the transcript and returns a VideoFileClip

## Functions

### Utils

```python
from owoi_audio_to_clip.utils import upload_audio_to_gcs, upload_video_to_gcs, purge_local_storage_images

upload_audio_to_gcs(bucket_name, username, audio_name, local_storage_path)
upload_video_to_gcs(bucket_name, username, video_name, local_storage_path)
purge_local_storage_images(local_storage_path)
download_audio_from_youtube(youtube_url, local_dest, username, audio_name, start_time, end_time, gcs_bucket_name)
```

#### download_audio_from_youtube

This function is used to download an audio file from a youtube video, and upload it to the gcs bucket.

Params:
- ***youtube_url***:str -> url of the youtube video
- ***local_dest***:str -> path to the local storage destination (where the audio file will be downloaded, the program will create a folder with the username, and put the audio in an 'audios' folder)
- ***username***:str -> name of the user
- ***audio_name***:str -> name of the audio file
- ***start_time***:str -> start time of the audio file extracted from the youtube video
- ***end_time***:str -> end time of the audio file extracted from the youtube video
- ***gcs_bucket_name***:str -> name of the gcs bucket destination