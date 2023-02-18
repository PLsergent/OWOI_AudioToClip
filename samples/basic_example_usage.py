import sys

sys.path.insert(0, "..")
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory
from owoi_audio_to_clip.utils import (
    upload_audio_to_gcs,
    upload_video_to_gcs,
    purge_local_storage_images,
    download_audio_from_youtube,
)

download_audio_from_youtube("https://www.youtube.com/watch?v=d-JBBNg8YKs", "../tmp/", "username", "sicko_mode", 25, 50, "owoi_bucket")

# upload_audio_to_gcs("owoi_bucket", "username", "sicko_mode", "../tmp/")
# print("Audio upload done!")

transcript_factory_test = TranscriptFactory("gs://owoi_bucket/username/audios/sicko_mode.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

print(transcript)

clip_maker_factory = ClipMakerFactory("sicko_mode", "username", transcript, "owoi_bucket", "../tmp/", "sicko_mode")

lip = clip_maker_factory.clip_maker()

# upload_video_to_gcs("owoi_bucket", "username", "sicko_mode", "../tmp/")
# print("Video upload done!")

# purge_local_storage_images("../tmp/")