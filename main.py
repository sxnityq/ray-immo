import os
import numpy as np
from tqdm import tqdm

import boto3
import cv2

REGION = "us-east-2"


class S3Downloader:
    
    def __init__(self, region=REGION):
        self.client = boto3.client("s3", region_name=region)

    def get_files(self, bucket: str="ray-first") -> list:
        content = self.client.list_objects_v2(
            Bucket=bucket)
    
        files = []
    
        for file in content.get("Contents"):
            if file.get("Key").startswith("input/") and file.get("Size") != 0:
                files.append(file.get("Key"))
            elif len(files) > 0:
                break
    
        return files        

    def download_files(self, bucket: str="ray-first") -> None:
        os.makedirs(name="tmp", mode=511, exist_ok=True)
        for file in self.get_files():
            self.client.download_file(
                Bucket=bucket,
                Key=file,
                Filename=f"tmp/{file.split('/')[-1]}"
                )
    
    def process_files(self) -> None:
        if not os.path.exists("tmp"):
            raise FileNotFoundError(f"folder tmp does not exist")
        for file in os.listdir("tmp"):
            os.makedirs(
                name=f"output/{file}-opencv",
                mode=511,
                exist_ok=True)
            
            cap = cv2.VideoCapture(os.path.join("tmp", file))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            video_height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            video_width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            
            print(f"video heigth: {video_height}")
            print(f"video width: {video_width}")
            print(f"processing: {file}")
            print(f"fps: {fps}")
            print(f"frames: {frames}")
            
            count = 0
            while True:
                is_read, frame = cap.read()
                if not is_read:
                    break
                cv2.imwrite(os.path.join(f"output/{file}-opencv", f"{count}-frame.jpg"), frame) 
                count += 1
            
            print("=======putting grid on photos=======")
            
            for frame in tqdm(os.listdir(f"output/{file}-opencv")):
                img = cv2.imread(os.path.join(f"output/{file}-opencv", frame))
                img = self.draw_grid(img, (25, 25))
                cv2.imwrite(os.path.join(f"output/{file}-opencv", frame), img)
            
            print("========assembling video from frames========")
            
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video = cv2.VideoWriter(
                filename=f"output/{file}",
                fourcc=fourcc,
                fps=fps,
                frameSize=(video_width, video_height))
            for frame in tqdm(sorted(os.listdir(f"output/{file}-opencv"), key=lambda x: int(x.split("-")[0]))):
                img = cv2.imread(os.path.join(f"output/{file}-opencv", frame))
                video.write(img)
    
    @staticmethod
    def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
        h, w, _ = img.shape
        rows, cols = grid_shape
        dy, dx = h / rows, w / cols

        for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
            x = int(round(x))
            cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)
            
        for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
            y = int(round(y))
            cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)
        return img

s3 = S3Downloader()
s3.download_files()
s3.process_files()
