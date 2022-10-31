from dataclasses import dataclass
import os
import traceback
from moviepy.editor import AudioFileClip, VideoFileClip

from audio_to_clip.WordTimestamp import WordTimestamp

@dataclass
class ClipMakerFactory:
    words_timestamps: list[WordTimestamp]
    google_credentials_key: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def get_audio_file(self, filename: str) -> AudioFileClip:
        try:
            os.makedirs("./tmp/", exist_ok=True)
            bucket = self.storage_client.bucket(self.gcs_uri)
            blob = bucket.blob(filename)
            blob.download_to_filename("./tmp/" + filename)
            return AudioFileClip("./tmp/" + filename)
        except:
            traceback.print_exc()
            raise Exception("Could not download audio file from GCS")