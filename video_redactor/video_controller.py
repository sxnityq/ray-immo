import os
from dotenv import load_dotenv
import ray
from .video_processor import VideoProcessor

load_dotenv()
project_dir = os.environ["WORK_DIRECTORY"]


class VideoController:
    
    def process_videos(self, client):
        client.download_files()

        futures = []

        # prcess = VideoProcessor()
        # futures.append(prcess.small_ml().remote())

        for file in os.listdir(f"{project_dir}/tmp"):
            if not os.path.exists(f"{project_dir}/tmp/{file}"):
                raise FileExistsError(f"{file} does not exist in tmp folder. Check it for more details")
            else:
                processor = VideoProcessor.remote(file)
                futures.append(processor.create_grid_video.remote())
                # second worker work over the same video
                futures.append(processor.stabilize_video.remote())

        ray.get(futures)
        #client.upload_output()
