from dataclasses import dataclass, field
import os
import traceback
from google.cloud import speech
from google.cloud import storage

from owoi_audio_to_clip.WordTimestamp import WordTimestamp


@dataclass
class TranscriptFactory:
    gcs_uri: str
    language_code: str = "en-US"
    word_timestamps: list[WordTimestamp] = field(default_factory=list)
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
            if len(self.word_timestamps) == 0:
                raise Exception("Could not transcribe audio to text")
            self._fill_blanks()
            return self.word_timestamps
        except:
            traceback.print_exc()
            raise Exception("Could not transcribe audio to text")
    
    def _fill_blanks(self):
        self.word_timestamps.insert(0, WordTimestamp("###", 0, self.word_timestamps[0].start))
        for i in range(len(self.word_timestamps) - 1):
            if self.word_timestamps[i].end == self.word_timestamps[i + 1].start:
                continue
            else:
                self.word_timestamps.insert(
                    i + 1,
                    WordTimestamp(
                        "###", self.word_timestamps[i].end, self.word_timestamps[i + 1].start
                    ),
                )

    def get_word_timestamps(self):
        return self.word_timestamps
