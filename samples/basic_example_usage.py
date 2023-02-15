import sys
sys.path.insert(0,"..")
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory


transcript_factory_test = TranscriptFactory("gs://owoi_bucket/test_audio/rap_god.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

print(transcript)

clip_maker_factory = ClipMakerFactory("rap_god", "username", transcript, "owoi_bucket", "../tmp/", "test_audio/rap_god.wav")

clip = clip_maker_factory.clip_maker()