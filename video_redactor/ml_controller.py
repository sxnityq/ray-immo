import os
from dotenv import load_dotenv
import ray
from video_redactor.small_ml import Small_ML


class MLController:
    def __init__(self):
        ray.init()

    def process_ml(self):
        futures = []
        ml = Small_ML.remote()
        for _ in range(2):
            futures.append(ml.process.remote())

        ray.get(futures)
