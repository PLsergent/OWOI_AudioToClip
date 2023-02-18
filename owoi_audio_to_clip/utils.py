from google.cloud import storage
from pytube import YouTube
from moviepy.editor import AudioFileClip

import os


def upload_video_to_gcs(gcs_bucket, username, video_name, local_dest):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(f"{username}/videos/{video_name}.mp4")
    blob.upload_from_filename(f"{local_dest}/{username}/videos/{video_name}.mp4")

def upload_audio_to_gcs(gcs_bucket, username, audio_name, local_dest):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(f"{username}/audios/{audio_name}.wav")
    blob.upload_from_filename(f"{local_dest}/{username}/audios/{audio_name}.wav")

def purge_local_storage_images(local_dest):
    for file in os.listdir(local_dest):
        if file.endswith(".jpg"):
            os.remove(os.path.join(local_dest, file))

def download_audio_from_youtube(youtube_url, local_dest, username, audio_name, start_time, end_time, gcs_bucket_name):
    os.makedirs(f"{local_dest}/{username}/audios", exist_ok=True)
    out_file = YouTube(youtube_url).streams.get_audio_only().download(output_path=f"{local_dest}/{username}/audios", filename=audio_name)
    base, _ = os.path.splitext(out_file)
    new_file = base + '.wav'
    os.rename(out_file, new_file)

    audio_file_clip = AudioFileClip(f"{local_dest}/{username}/audios/{audio_name}.wav", fps=44100, nbytes=4, buffersize=13000000)
    audio_file_clip = audio_file_clip.subclip(start_time, end_time)
    audio_file_clip.write_audiofile(f"{local_dest}/{username}/audios/{audio_name}.wav", fps=44100, nbytes=4, buffersize=13000000, bitrate="500k")
    upload_audio_to_gcs(gcs_bucket_name, username, audio_name, local_dest)