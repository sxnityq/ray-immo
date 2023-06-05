import os
from time import time

from dotenv import load_dotenv
import ray

from video_redactor.aws import S3Client
from video_redactor.video_controller import VideoController


load_dotenv()
project_dir = os.environ["WORK_DIRECTORY"]


if __name__ == "__main__":

    start = time()
    
    #it needs for storing videos inside remote clusters. Keep empty on local machine
    #down overwrite either
    if not os.path.exists(f"{os.environ['WORK_DIRECTORY']}/output"):
        os.mkdir(os.path.join(project_dir, "output"))
    if not os.path.exists(f"{os.environ['WORK_DIRECTORY']}/input"):
        os.mkdir(os.path.join(project_dir, "input"))

    client = S3Client(bucket="ray-first")
    #print("download files")
    #client.download_files()

    ray.init(address="ray://44.211.217.38:10001", runtime_env={
        "working_dir": project_dir,
        "pip": os.path.join(project_dir, "requirements.txt"),
        "env_vars": {
            'WORK_DIRECTORY': os.environ['WORK_DIRECTORY'],
            'AWS_ACCESS_KEY': os.environ['AWS_ACCESS_KEY'],
            'AWS_SECRET_ACCESS_KEY': os.environ['AWS_SECRET_ACCESS_KEY']}
            }
        )
    
    print('''This cluster consists of
    {} nodes in total
    {} CPU resources in total
'''.format(len(ray.nodes()), ray.cluster_resources()['CPU']))
    
    print("processing files")

    controller = VideoController()
    controller.process_videos(client)
    
    print(time() - start)
    print("finish processing")
    ray.shutdown()
