from dataclasses import dataclass
import os
import traceback
from google.cloud import speech
from google.cloud import storage

from owoi_audio_to_clip.WordTimestamp import WordTimestamp


@dataclass
class TranscriptFactory:
    gcs_uri: str
    language_code: str = "en-US"
    word_timestamps: list[WordTimestamp] = []
    speech_client = speech.SpeechClient()
    storage_client = storage.Client()
    google_credentials_key: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def _get_recognition_config(self):
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=self.language_code,
            sample_rate_hertz=44100,
            audio_channel_count=2,
            enable_word_time_offsets=True,
            use_enhanced=True,
            model="video",
        )

    def transcribe_audio_to_text(self) -> list[WordTimestamp]:
        self.word_timestamps = []
        try:
            operation = self.speech_client.long_running_recognize(
                config=self._get_recognition_config(),
                audio=speech.RecognitionAudio(uri=self.gcs_uri),
            )
            response = operation.result()

            for result in response.results:
                alternative = result.alternatives[0]
                for word_info in alternative.words:
                    self.word_timestamps.append(
                        WordTimestamp(
                            word_info.word, word_info.start_time, word_info.end_time
                        )
                    )
            return self.word_timestamps
        except:
            traceback.print_exc()
            raise Exception("Could not transcribe audio to text")

    def get_word_timestamps(self):
        return self.word_timestamps
