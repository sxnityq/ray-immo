import os

from dotenv import load_dotenv
from video_redactor.video_processor import VideoProcessor
from video_redactor.aws import S3Client
from tqdm import tqdm


load_dotenv()


if __name__ == "__main__":
    client = S3Client(bucket="ray-first", region="us-east-2")
    client.download_files()
    
    for file in os.listdir(f"{os.environ['WORK_DIRECTORY']}/tmp"):
        processor = VideoProcessor(file)
        processor.process_video()
    