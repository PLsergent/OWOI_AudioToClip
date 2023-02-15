import sys
sys.path.insert(0,"..")
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory


transcript_factory_test = TranscriptFactory("gs://owoi_bucket/test_audio/tell_me_which_one.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

print(transcript)

clip_maker_factory = ClipMakerFactory("test_video", "username", transcript, "owoi_bucket", "../tmp/", "test_audio/tell_me_which_one.wav")

clip = clip_maker_factory.clip_maker()