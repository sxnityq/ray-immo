import os
from time import time

from dotenv import load_dotenv
import ray

from video_redactor.aws import S3Client
from video_redactor.video_controller import VideoController
from video_redactor.video_processor import VideoProcessor


load_dotenv()


if __name__ == "__main__":
    ray.init()
    client = S3Client(bucket="ray-first", region="us-east-2")
    
    start = time()
    
    print("downloading files")
    client.download_files()
    
    print("processing files")
    futures = []
    for file in os.listdir(f"{os.environ['WORK_DIRECTORY']}/tmp"):
        processor = VideoProcessor.remote(file)
        futures.append(processor.process_video.remote())
        print("uploading files")
    
    ray.get(futures)
    print('uploading')
    client.upload_output()
    
    end = time() - start
    print(end)

    #controller = VideoController()

    #controller.process_videos(client)
    