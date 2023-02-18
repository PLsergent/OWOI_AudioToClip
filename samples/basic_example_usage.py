import sys
sys.path.insert(0,"..")
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory
from owoi_audio_to_clip.utils import upload_audio_to_gcs, upload_video_to_gcs, purge_local_storage_images


upload_audio_to_gcs("owoi_bucket", "username", "lose_yourself", "../tmp/")
print("Audio upload done!")

transcript_factory_test = TranscriptFactory("gs://owoi_bucket/username/audios/lose_yourself.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

print(transcript)

clip_maker_factory = ClipMakerFactory("lose_yourself", "username", transcript, "owoi_bucket", "../tmp/", "lose_yourself")

clip = clip_maker_factory.clip_maker()

upload_video_to_gcs("owoi_bucket", "username", "lose_yourself", "../tmp/")
print("Video upload done!")

# purge_local_storage_images("../tmp/")