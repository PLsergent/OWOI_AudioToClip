from owoi_audio_to_clip.TranscriptFactory import TranscriptFactory


test = TranscriptFactory("gs://owoi_bucket/test_audio/sinatra.wav")

print(test.transcribe_audio_to_text())