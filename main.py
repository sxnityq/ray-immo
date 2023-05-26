from time import time

from video_redactor.aws import S3Client
from video_redactor.video_controller import VideoController

if __name__ == "__main__":
    client = S3Client(bucket="ray-first", region="us-east-2")

    start = time()

    print("downloading files")
    client.download_files()

    print("processing files")
    controller = VideoController()
    controller.process_videos(client)

    end = time() - start
    print(end)
