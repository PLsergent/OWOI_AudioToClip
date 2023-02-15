from dataclasses import dataclass
import os
import traceback
import requests
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, ColorClip, concatenate_videoclips
from google.cloud import storage
from google_images_search import GoogleImagesSearch

from owoi_audio_to_clip.WordTimestamp import WordTimestamp


@dataclass
class ClipMakerFactory:
    video_name: str
    username: str
    words_timestamps: list[WordTimestamp]
    gcs_bucket: str
    local_dest: str
    gcs_audio_path: str
    audio_file_clip: AudioFileClip = None
    video_file_clip: VideoFileClip = None
    storage_client = storage.Client()
    google_images_search_token = os.environ.get("GOOGLE_IMAGES_SEARCH_TOKEN")
    google_search_id = os.environ.get("GOOGLE_SEARCH_ID")
    google_credentials_key: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def _get_audio_file(self, path_to_gcs: str) -> AudioFileClip:
        if self.audio_file_clip is not None:
            return self.audio_file_clip
        try:
            os.makedirs(self.local_dest, exist_ok=True)
            bucket = self.storage_client.bucket(self.gcs_bucket)
            blob = bucket.blob(path_to_gcs)
            filename = path_to_gcs.split("/")[-1]
            blob.download_to_filename(self.local_dest + filename)
            return AudioFileClip(self.local_dest + filename)
        except:
            traceback.print_exc()
            raise Exception("Could not download audio file from GCS")
    
    def clip_maker(self) -> VideoFileClip:
        try:
            clips = [self._define_image_clip(wordts.get_word_dict()) for wordts in self.words_timestamps]
            self.video_file_clip = concatenate_videoclips(clips, method="compose")
            self.video_file_clip = self.video_file_clip.set_audio(self._get_audio_file(self.gcs_audio_path))
            self.video_file_clip.write_videofile(
                self.local_dest + self.video_name + ".mp4", fps=24, codec="mpeg4", bitrate="5000k"
            )
            return self.video_file_clip
        except:
            traceback.print_exc()
            raise Exception("Could not create video file clip")
    
    def _get_image_url_from_google_image_search(self, word: str, num: int = 1) -> str:
        gis = GoogleImagesSearch(self.google_images_search_token, self.google_search_id)
        _search_params = {
            'q': word,
            'num': num,
            'imgSize': 'xlarge',
            'safe': 'active',
            'imgColorType': 'color'
        }
        gis.search(search_params=_search_params)
        if len(gis.results()) == 0:
            return "https://img.freepik.com/premium-vector/website-page-found-error-robot-character-with-magnifying-glass-hand-site-crash-technical_502272-1890.jpg?w=2000"
        return gis.results()[num-1].url
    
    def _define_image_clip(self, img_dict: dict) -> ImageClip:
        if img_dict['word'] == "###":
            color_clip = ColorClip((1920, 1080), (0,0,0))
            if img_dict["start"] == 0:
                color_clip = color_clip.set_duration(img_dict['end'].total_seconds())
            else:
                color_clip = color_clip.set_duration(img_dict['end'].total_seconds() - img_dict['start'].total_seconds())
            return color_clip

        num = 1
        image_clip = self._get_image_clip(img_dict, num)
        while image_clip is None:
            num += 1
            image_clip = self._get_image_clip(img_dict, num)
        return image_clip.set_duration(img_dict['end'].total_seconds() - img_dict['start'].total_seconds())
        
    def _get_image_clip(self, img_dict: dict, num: int):
        try:
            url = self._get_image_url_from_google_image_search(img_dict['word'], num=num)
            response = requests.get(url)
            open(self.local_dest + img_dict['word'] + '.jpg', 'wb').write(response.content)
            image_clip = ImageClip(self.local_dest + img_dict['word'] + '.jpg')
            return image_clip
        except:
            return None
    
    def upload_video_to_gcs(self):
        bucket = self.storage_client.bucket(self.gcs_bucket)
        blob = bucket.blob(f"{self.username}/{self.video_name}.mp4")
        blob.upload_from_filename(f"{self.local_dest}{self.username}/{self.video_name}.mp4")

    def get_video_file(self) -> VideoFileClip:
        if self.video_file_clip is not None:
            return self.video_file_clip
