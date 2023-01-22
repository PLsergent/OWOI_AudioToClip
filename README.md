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
from audio_to_clip import ClipMakerFactory

transcript_factory = TranscriptFactory(gcs_uri="gs://bucket/file.mp3")
```

Methods:
- ***transcribe_audio_to_text() -> list[dict]***: transcribe audio to text from the gcs_uri and returns a list of dict with the following keys: "word", "start_time" and "end_time"
- ***get_word_timestamps() -> list[dict]***: returns a list of dict with the following keys: "word", "start_time" and "end_time"

This Class should be used to create a transcript from a text file before creating a clip with the ClipMakerFactory.

### ClipMakerFactory

This class is used to create a clip from a transcript.

```python
from audio_to_clip import ClipMakerFactory

clip_makfer_factory = ClipMagerFactory(video_name, username, transcript, gcs_bucket_dest, local_storage_dest, gcs_bucket_audio)
```

Params:
- ***video_name***:str -> name of the video
- ***username***:str -> name of the user
- ***transcript***:list[WordTimestamp] -> list of WordTimestamp
- ***gcs_bucket_dest***:str -> name of the gcs bucket destination
- ***local_storage_dest***:str -> path to the local storage destination
- ***gcs_bucket_audio***:str -> name of the gcs bucket where the audio is stored

Methods:
- ***clip_maker(word_timestamps: list[WordTimestamp]) -> VideoFileClip***: creates a clip from the transcript and returns a VideoFileClip
- ***upload_video_to_gcs() -> None***: uploads the video to the gcs bucket with the name: `username/video_name.mp4`, should be called after clip_maker