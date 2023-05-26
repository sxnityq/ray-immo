import ray
import os
from ray import tune
from video_redactor.video_processor import VideoProcessor


class VideoController:
    def __init__(self):
        self.worker = VideoProcessor()

    def process_videos(self, client):
        client.download_files()

        video_files = client.get_files(bucket="ray-first")
        analysis = tune.run(
            tune.with_parameters(self.worker.process_video),
            config={"video_path": tune.grid_search(video_files),
                    "output_path": os.path.join(os.environ['WORK_DIRECTORY'], "output", "{=output_path}")},
            resources_per_trial={"cpu": 1, "gpu": 0},
            num_samples=len(video_files)
        )

        client.upload_output()

    def shutdown(self):
        self.worker.shutdown()
