import os
from dotenv import load_dotenv
import ray
from video_redactor.small_ml import Small_ML

load_dotenv()
project_dir = os.environ["WORK_DIRECTORY"]


class MLController:
    def __init__(self):
        ray.init()

    def process_ml(self):
        futures = []
        ml = Small_ML()
        for _ in range(2):
            futures.append(ml.small_ml().remote())

        ray.get(futures)
