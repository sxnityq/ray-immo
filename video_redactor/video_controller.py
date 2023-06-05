import ray

from .video_processor import VideoProcessor


class VideoController:

    def process_videos(self, client):
        
        files = client.get_files()
        futures = []

        for file in files:
            processor = VideoProcessor.remote(video=file, client=client)
            futures.append(processor.create_grid_video.remote())
            # second worker work over the same video
            #futures.append(processor.stabilize_video.remote())

        ray.get(futures)



