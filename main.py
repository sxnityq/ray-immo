import os
from time import time

from dotenv import load_dotenv
import ray

from video_redactor.aws import S3Client
from video_redactor.video_controller import VideoController


load_dotenv()
project_dir = os.environ["WORK_DIRECTORY"]


if __name__ == "__main__":
    os.makedirs(
        name=f"{project_dir}/output",
        mode=511,
        exist_ok=True)
    client = S3Client(bucket="ray-first", region="us-east-2")
    ray.init()
    start = time()

    print("processing files")
    controller = VideoController()
    controller.process_videos(client)

    print(time() - start)
    ray.shutdown()
