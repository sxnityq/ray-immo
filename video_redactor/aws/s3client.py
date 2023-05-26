import os

import boto3
from dotenv import load_dotenv


load_dotenv()


class S3Client:
    def __init__(self, bucket: str="ray-first", region: str="us-east-2"):
        session = boto3.Session(
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=region)
        self.bucket = bucket
        self.s3_client = session.client('s3')

    def get_files(self, bucket: str="ray-first") -> list:
        content = self.s3_client.list_objects_v2(
            Bucket=bucket)
    
        files = []
    
        for file in content.get("Contents"):
            if file.get("Key").startswith("input/") and file.get("Size") != 0:
                files.append(file.get("Key"))
            elif len(files) > 0:
                break
    
        return files
    
    def download_files(self) -> None:
        os.makedirs(name=f"{os.environ['WORK_DIRECTORY']}/tmp", mode=511, exist_ok=True)
        for file in self.get_files():
            self.s3_client.download_file(
                Bucket=self.bucket,
                Key=file,
                Filename=f"{os.environ['WORK_DIRECTORY']}/tmp/{file.split('/')[-1]}"
                )
            
    def upload_output(self):
        if not os.path.exists(f"{os.environ['WORK_DIRECTORY']}/output"):
            raise FileExistsError("Can't get output dir to deploy. Check it's existense")
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key="output/",
            Body=""
        )
        for file in os.listdir(f"{os.environ['WORK_DIRECTORY']}/output"):
            self.s3_client.upload_file(
                f"{os.environ['WORK_DIRECTORY']}/output/{file}",
                self.bucket,
                f"output/{file}")

__all__ = ("S3Client", )

if __name__ == "__main__":
    client = S3Client(bucket="ray-first", region="us-east-2")
    client.upload_output()