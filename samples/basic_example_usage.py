import sys
sys.path.insert(0,"..")
from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory
from owoi_audio_to_clip.ClipMakerFactory import ClipMakerFactory


transcript_factory_test = TranscriptFactory("gs://owoi_bucket/test_audio/sinatra.wav")

transcript = transcript_factory_test.transcribe_audio_to_text()

clip_maker_factory = ClipMakerFactory("test_video", "username", transcript, "owoi_bucket", "../tmp/", "test_audio/sinatra.wav")

clip = clip_maker_factory.clip_maker()