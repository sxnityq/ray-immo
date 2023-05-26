import ray
from video_redactor.video_processor import VideoProcessor


class VideoController:
    def __init__(self):
        ray.init()

    def process_videos(self, client):
        client.download_files()

        video_files = client.get_files(bucket="ray-first")
        futures = []
        for file in video_files:
            processor = VideoProcessor.remote(file)
            futures.append(processor.process_video.remote())

        ray.get(futures)
        client.upload_output()

        self.shutdown()

    def shutdown(self):
        ray.shutdown()
