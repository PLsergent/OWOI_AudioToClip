from google.cloud import storage
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
