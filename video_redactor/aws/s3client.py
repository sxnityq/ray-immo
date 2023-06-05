import os
import boto3
from dotenv import load_dotenv
import pickle

load_dotenv()

session = boto3.Session(
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name="us-east-2")

client = session.client('s3')

class S3Client:
    def __init__(self, bucket: str="ray-first"):
        self.bucket = bucket

    def get_files(self, bucket: str="ray-first") -> list:
        content = client.list_objects_v2(
            Bucket=bucket)
    
        files = []
    
        for file in content.get("Contents"):
            if file.get("Key").startswith("input/") and file.get("Size") != 0:
                files.append(file.get("Key"))
            elif len(files) > 0:
                break
    
        return files
    
    #need to fix later
    def download_files(self) -> None:
        if not os.path.exists(f"{os.environ['WORK_DIRECTORY']}/input"):
            os.mkdir(f"{os.environ['WORK_DIRECTORY']}/input")
        for file in self.get_files():
            client.download_file(
                Bucket=self.bucket,
                Key=file,
                Filename=f"{os.environ['WORK_DIRECTORY']}/input/{file.split('/')[-1]}"
                )

    def download_file(self, file, remote=False) -> None:
        if remote:
            workdir = os.getcwd()
        else:
            workdir = {os.environ['WORK_DIRECTORY']}
        if not os.path.exists(f"{workdir}/input"):
            os.mkdir(f"{workdir}/input")
        client.download_file(
            Bucket=self.bucket,
            Key=file,
            Filename=f"{workdir}/{file}"
            )
    
    #need to fix later
    def upload_output(self):
        if not os.path.exists(f"{os.environ['WORK_DIRECTORY']}/output"):
            raise FileExistsError("Can't get output dir to deploy. Check it's existense")
        client.put_object(
            Bucket=self.bucket,
            Key="output/",
            Body=""
        )
        for file in os.listdir(f"{os.environ['WORK_DIRECTORY']}/output"):
            client.upload_file(
                f"{os.environ['WORK_DIRECTORY']}/output/{file}",
                self.bucket,
                f"output/{file}"
                )
    
    def upload_file(self, video):
        client.upload_file(
            video,
            self.bucket,
            f"output/{video.rsplit('/', maxsplit=1)[-1]}"
            )

__all__ = ("S3Client", "client")

if __name__ == "__main__":
    client = S3Client(bucket="ray-first", region="us-east-2")
    pickle.dumps(client)
    #client.upload_output()