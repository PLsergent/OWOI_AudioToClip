from dataclasses import dataclass
import os
import traceback
import requests
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip
from google.cloud import storage
from google_images_search import GoogleImagesSearch

from owoi_audio_to_clip.WordTimestamp import WordTimestamp


@dataclass
class ClipMakerFactory:
    video_name: str
    username: str
    words_timestamps: list[WordTimestamp]
    gcs_bucket_dest: str
    local_dest: str
    gcs_bucket_audio: str
    audio_file_clip: AudioFileClip = None
    video_file_clip: VideoFileClip = None
    images: list[str] = []
    storage_client = storage.Client()
    google_images_search_token = os.environ.get("GOOGLE_IMAGES_SEARCH_TOKEN")
    google_search_id = os.environ.get("GOOGLE_SEARCH_ID")
    google_credentials_key: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def _get_audio_file(self, filename: str) -> AudioFileClip:
        if self.audio_file_clip is not None:
            return self.audio_file_clip
        try:
            os.makedirs("./tmp/", exist_ok=True)
            bucket = self.storage_client.bucket(self.gcs_bucket_audio)
            blob = bucket.blob(filename)
            blob.download_to_filename("./tmp/" + filename)
            return AudioFileClip("./tmp/" + filename)
        except:
            traceback.print_exc()
            raise Exception("Could not download audio file from GCS")
    
    def clip_maker(self, word_timestamps: list[WordTimestamp]) -> VideoFileClip:
        try:
            for wordts in word_timestamps:
                self.images.append(wordts.get_word_dict())
            
            clips = [self._define_image_clip(img_dict) for img_dict in self.images]
            self.video_file_clip = VideoFileClip.concatenate_videoclips(clips)
            self.video_file_clip.write_videofile(
                self.local_dest + self.video_name + ".mp4", fps=24, codec="mpeg4"
            )
            self.video_file_clip.set_audio(self._get_audio_file(self.video_name + ".mp3"))
            return self.video_file_clip
        except:
            traceback.print_exc()
            raise Exception("Could not create video file clip")
    
    def _get_image_url_from_google_image_search(self, word: str) -> str:
        gis = GoogleImagesSearch(self.google_images_search_token, self.google_search_id)
        _search_params = {
            'q': word,
            'num': 1,
            'safe': 'off',
            'fileType': 'png',
            'imgType': 'photo',
            'imgSize': 'MEDIUM',
            'rights': 'cc_publicdomain'
        }
        gis.search(search_params=_search_params)
        return gis.results()[0].url
    
    def _define_image_clip(self, img_dict: dict) -> ImageClip:
        url = self._get_image_url_from_google_image_search(img_dict['word'])
        response = requests.get(url)
        open(self.local_dest + img_dict['word'] + '.png', 'wb').write(response.content)
        return ImageClip(
                    self.local_dest + img_dict['word'] + '.png'
                ).set_duration(img_dict['end_time'] - img_dict['start_time'])
    
    def upload_video_to_gcs(self):
        bucket = self.storage_client.bucket(self.gcs_bucket_dest)
        blob = bucket.blob(f"{self.username}/{self.video_name}.mp4")
        blob.upload_from_filename(f"{self.local_dest}{self.username}/{self.video_name}.mp4")

    def get_video_file(self) -> VideoFileClip:
        if self.video_file_clip is not None:
            return self.video_file_clip
