import sys
sys.path.insert(0,"..")
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory
from owoi_audio_to_clip.utils import upload_audio_to_gcs, upload_video_to_gcs, purge_local_storage_images


upload_audio_to_gcs("owoi_bucket", "username", "tell_me_which_one", "../tmp/")
print("Audio upload done!")

transcript_factory_test = TranscriptFactory("gs://owoi_bucket/username/audios/tell_me_which_one.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

print(transcript)

clip_maker_factory = ClipMakerFactory("tell_me_which_one", "username", transcript, "owoi_bucket", "../tmp/", "tell_me_which_one")

clip = clip_maker_factory.clip_maker()

# upload_video_to_gcs("owoi_bucket", "username", "tell_me_which_one", "../tmp/")
print("Video upload done!")

# purge_local_storage_images("../tmp/")