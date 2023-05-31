import os
import cv2
import ray
import numpy as np
from dotenv import load_dotenv

load_dotenv()
project_dir = os.environ["WORK_DIRECTORY"]


@ray.remote
class VideoProcessor:

    def __init__(self, video):
        """pass relative path to video in tmp folder otherwise cause implicit errors"""
        self.video = video
        self.output_video = f"{project_dir}/output/{self.video}"

    @staticmethod
    def _draw_grid(frame, grid_shape=(25, 25), color=(0, 255, 0), thickness=1) -> None:
        h, w, _ = frame.shape
        rows, cols = grid_shape
        dy, dx = h / rows, w / cols

        for x in np.linspace(start=dx, stop=w - dx, num=cols - 1):
            x = int(round(x))
            cv2.line(frame, (x, 0), (x, h), color=color, thickness=thickness)

        for y in np.linspace(start=dy, stop=h - dy, num=rows - 1):
            y = int(round(y))
            cv2.line(frame, (0, y), (w, y), color=color, thickness=thickness)

    def create_grid_video(self):
        cap = cv2.VideoCapture(f"{project_dir}/tmp/{self.video}")
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
            filename=self.output_video,
            fourcc=cv2.VideoWriter_fourcc(*'mp4v'),
            fps=fps,
            frameSize=(video_width, video_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self._draw_grid(frame)
            output_video.write(frame)

        cap.release()
        output_video.release()
        print(f"finish processing: {self.video}")

    def make_gray(self):
        cap = cv2.VideoCapture(self.video)
        output_video = cv2.VideoWriter(
            self.output_video,
            cv2.VideoWriter_fourcc(*'mp4v'),
            int(cap.get(cv2.CAP_PROP_FPS)),
            (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
             int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
            isColor=False)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            output_video.write(gray_frame)

        cap.release()
        output_video.release()

    def stabilize_video(self):
        cap = cv2.VideoCapture(self.video_file)
        _, prev_frame = cap.read()

        height, width, _ = prev_frame.shape

        output = cv2.VideoWriter(
            self.output,
            cv2.VideoWriter_fourcc(*"mp4v"),
            30,
            (width,
             height))

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        while True:
            ret, frame = cap.read()

            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            orb = cv2.ORB_create()
            keypoints_prev, descriptors_prev = orb.detectAndCompute(prev_gray, None)
            keypoints_curr, descriptors_curr = orb.detectAndCompute(gray, None)

            matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
            matches = matcher.match(descriptors_prev, descriptors_curr, None)

            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = matches[:int(len(matches) * 0.2)]

            src_pts = np.float32([keypoints_prev[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_curr[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            transform_matrix, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC)

            stabilized_frame = cv2.warpAffine(frame, transform_matrix, (width, height))

            output.write(stabilized_frame)

            prev_gray = gray

        cap.release()
        output.release()
