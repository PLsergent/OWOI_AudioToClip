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

download_audio_from_youtube("https://youtu.be/mprkqDNUQb0", "../tmp", "username", "maad_city", 0, 20, "owoi_bucket")

# upload_audio_to_gcs("owoi_bucket", "username", "maad_city", "../tmp/")
# print("Audio upload done!")

transcript_factory_test = TranscriptFactory("gs://owoi_bucket/username/audios/maad_city.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

print(transcript)

clip_maker_factory = ClipMakerFactory("maad_city", "username", transcript, "owoi_bucket", "../tmp", "maad_city", with_subtitles=True)

clip = clip_maker_factory.clip_maker()

# upload_video_to_gcs("owoi_bucket", "username", "maad_city", "../tmp/")
# print("Video upload done!")

# purge_local_storage_images("../tmp/")