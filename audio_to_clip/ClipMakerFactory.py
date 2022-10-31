from dataclasses import dataclass
import os
import traceback
from moviepy.editor import AudioFileClip, VideoFileClip

from audio_to_clip.WordTimestamp import WordTimestamp

@dataclass
class ClipMakerFactory:
    video_name: str
    username: str
    words_timestamps: list[WordTimestamp]
    audio_file_clip: AudioFileClip = None
    video_file_clip: VideoFileClip = None
    gcs_storage_uri: str = f"gs://videos/{username}/{video_name}"
    google_credentials_key: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def get_audio_file(self, filename: str) -> AudioFileClip:
        if self.audio_file_clip is not None:
            return self.audio_file_clip
        try:
            os.makedirs("./tmp/", exist_ok=True)
            bucket = self.storage_client.bucket(self.gcs_uri)
            blob = bucket.blob(filename)
            blob.download_to_filename("./tmp/" + filename)
            return AudioFileClip("./tmp/" + filename)
        except:
            traceback.print_exc()
            raise Exception("Could not download audio file from GCS")
    
    def get_video_file(self) -> VideoFileClip:
        if self.video_file_clip is not None:
            return self.video_file_clip
