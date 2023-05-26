import os

from dotenv import load_dotenv

from video_redactor.aws import S3Client
from video_redactor.video_controller import VideoController
from video_redactor.video_processor import VideoProcessor


load_dotenv()


if __name__ == "__main__":
    client = S3Client(bucket="ray-first", region="us-east-2")
    #
    # print("downloading files")
    # client.download_files()
    #
    # print("processing files")
    # for file in os.listdir(f"{os.environ['WORK_DIRECTORY']}/tmp"):
    #     processor = VideoProcessor(file)
    #     processor.process_video()
    #
    # print("uploading files")
    # client.upload_output()

    controller = VideoController()

    controller.process_videos(client)
    