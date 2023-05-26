import os

from dotenv import load_dotenv
import ray

from .video_processor import VideoProcessor

#load_dotenv()
#project_dir = os.environ["WORK_DIRECTORY"]

class VideoController:
    
    def process_videos(self, client):
        client.download_files()

        video_files = client.get_files(bucket="ray-first")
        futures = []
        for file in video_files:
            processor = VideoProcessor.remote(file)
            futures.append(processor.process_video.remote())

        ray.get(futures)
        client.upload_output()
