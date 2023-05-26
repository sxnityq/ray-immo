import os

import cv2
import ray
from dotenv import load_dotenv
import numpy as np


load_dotenv()

@ray.remote
class VideoProcessor:
    def __init__(self, video):
        self.video = video

    def process_video(self):
        os.makedirs(
            name=f"{os.environ['WORK_DIRECTORY']}/output",
            mode=511,
            exist_ok=True)
        if os.path.exists(f"{os.environ['WORK_DIRECTORY']}/tmp/{self.video}"):
            cap = cv2.VideoCapture(f"{os.environ['WORK_DIRECTORY']}/tmp/{self.video}")
        else:
            raise FileExistsError(f"{self.video} does not exist. Check tmp folder for details")
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        video_height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            
        print(f"processing: {self.video}")
        print(f"video heigth: {video_height}")
        print(f"video width: {video_width}")
        print(f"fps: {fps}")
        print(f"frames: {frames}")
        
        output_video = cv2.VideoWriter(
            f"{os.environ['WORK_DIRECTORY']}/output/{self.video}",
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (video_width, video_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self._draw_grid(frame, (25, 25))
            output_video.write(frame)

        cap.release()
        output_video.release()
        cv2.destroyAllWindows()
        print(f"finish processing: {self.video}")

    @staticmethod
    def _draw_grid(frame, grid_shape, color=(0, 255, 0), thickness=1) -> None:
        h, w, _ = frame.shape
        rows, cols = grid_shape
        dy, dx = h / rows, w / cols

        for x in np.linspace(start=dx, stop=w - dx, num=cols - 1):
            x = int(round(x))
            cv2.line(frame, (x, 0), (x, h), color=color, thickness=thickness)

        for y in np.linspace(start=dy, stop=h - dy, num=rows - 1):
            y = int(round(y))
            cv2.line(frame, (0, y), (w, y), color=color, thickness=thickness)

    def make_gray(self, input_path, output):
        video = cv2.VideoCapture(input_path)

        output_video = cv2.VideoWriter(
            output,
            cv2.VideoWriter_fourcc(*'mp4v'),
            int(video.get(cv2.CAP_PROP_FPS)),
            (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
             int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))),
            isColor=False)

        while True:
            ret, frame = video.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            output_video.write(gray_frame)

        video.release()
        output_video.release()

