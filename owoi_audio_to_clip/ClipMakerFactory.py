from dataclasses import dataclass
import os
import traceback
import requests
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    ImageClip,
    ColorClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from moviepy.video.tools.subtitles import SubtitlesClip

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
    gcs_audio_name: str
    with_subtitles: bool = False
    audio_file_clip: AudioFileClip = None
    video_file_clip: VideoFileClip = None
    storage_client = storage.Client()
    google_images_search_token = os.environ.get("GOOGLE_IMAGES_SEARCH_TOKEN")
    google_search_id = os.environ.get("GOOGLE_SEARCH_ID")
    google_credentials_key: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def _get_audio_file(self, audio_name: str) -> AudioFileClip:
        if self.audio_file_clip is not None:
            return self.audio_file_clip
        try:
            os.makedirs(f"{self.local_dest}/{self.username}/audios", exist_ok=True)
            bucket = self.storage_client.bucket(self.gcs_bucket)
            blob = bucket.blob(f"{self.username}/audios/{audio_name}.wav")
            blob.download_to_filename(
                f"{self.local_dest}/{self.username}/audios/{audio_name}.wav"
            )
            return AudioFileClip(
                f"{self.local_dest}/{self.username}/audios/{audio_name}.wav"
            )
        except:
            traceback.print_exc()
            raise Exception("Could not download audio file from GCS")

    def clip_maker(self) -> VideoFileClip:
        try:
            clips = [
                self._define_image_clip(wordts.get_word_dict())
                for wordts in self.words_timestamps
            ]
            self.video_file_clip = concatenate_videoclips(clips, method="compose")
            self.video_file_clip = self.video_file_clip.set_audio(
                self._get_audio_file(self.gcs_audio_name)
            )
            os.makedirs(f"{self.local_dest}/{self.username}/videos", exist_ok=True)
            if self.with_subtitles:
                self.video_file_clip = CompositeVideoClip(
                    [self.video_file_clip, self._generate_subtitles().set_pos(("center", "bottom"))]
                )
            self.video_file_clip.write_videofile(
                f"{self.local_dest}/{self.username}/videos/{self.video_name}.mp4",
                fps=24,
                codec="mpeg4",
                bitrate="5000k",
            )
            return self.video_file_clip
        except:
            traceback.print_exc()
            raise Exception("Could not create video file clip")

    def _generate_subtitles(self) -> SubtitlesClip:
        generator = lambda txt: TextClip(txt, bg_color="black", stroke_width=3, font="Arial", fontsize=72, color="yellow")
        subs = []
        for wordts in self.words_timestamps:
            word = wordts.get_word_dict()
            if word["word"] != "###":
                subs.append(
                    (
                        (word["start"].total_seconds(), word["end"].total_seconds()),
                        word["word"],
                    )
                )
        return SubtitlesClip(subs, generator).margin(bottom=40)

    def _get_image_url_from_google_image_search(self, word: str, num: int = 1, img_size: str = "xlarge") -> str:
        gis = GoogleImagesSearch(self.google_images_search_token, self.google_search_id)
        _search_params = {
            "q": word,
            "num": num,
            "imgSize": img_size,
            "safe": "medium",
            "imgColorType": "color",
        }
        gis.search(search_params=_search_params)
        if len(gis.results()) == 0:
            return "https://img.freepik.com/premium-vector/website-page-found-error-robot-character-with-magnifying-glass-hand-site-crash-technical_502272-1890.jpg?w=2000"
        return gis.results()[num - 1].url

    def _define_image_clip(self, wordts: dict) -> ImageClip:
        if wordts["word"] == "###":
            color_clip = ColorClip((1920, 1080), (0, 0, 0))
            if wordts["start"] == 0:
                color_clip = color_clip.set_duration(wordts["end"].total_seconds())
            else:
                color_clip = color_clip.set_duration(
                    wordts["end"].total_seconds() - wordts["start"].total_seconds()
                )
            return color_clip

        num = 1
        image_clip = self._get_image_clip(wordts, num)
        while image_clip is None:
            if num == 100:
                image_clip = ImageClip(
                    "https://img.freepik.com/premium-vector/website-page-found-error-robot-character-with-magnifying-glass-hand-site-crash-technical_502272-1890.jpg?w=2000"
                )
                break
            num += 1
            img_size = "large"
            image_clip = self._get_image_clip(wordts, num, img_size)
        return image_clip.set_duration(
            wordts["end"].total_seconds() - wordts["start"].total_seconds()
        )

    def _get_image_clip(self, wordts: dict, num: int, img_size: str = "xlarge"):
        try:
            for file in os.listdir(self.local_dest):
                if file == wordts["word"] + ".jpg":
                    return ImageClip(self.local_dest + wordts["word"] + ".jpg")
            url = self._get_image_url_from_google_image_search(wordts["word"], num=num, img_size=img_size)
            response = requests.get(url)
            open(self.local_dest + wordts["word"] + ".jpg", "wb").write(
                response.content
            )
            image_clip = ImageClip(self.local_dest + wordts["word"] + ".jpg")
            return image_clip
        except:
            return None
