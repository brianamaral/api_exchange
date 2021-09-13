import os 
import datetime
import json
import boto3

class DataWriter:
    def __init__(self, api: str,**kwargs) -> None:
        self.api = api
        self.filename = (
            f'{api}/{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.json'
        )
        self.file = self._open_file(self.filename)

    def _open_file(self, file):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        return open(file=file, mode="a")

    def _write_line(self, line: str) -> None:
        self.file.write(
            json.dumps(line, ensure_ascii=False).encode("latin-1").decode("latin-1")
            + "\n"
        )

    def _subdicts_into_dict(self, data: dict) -> iter:
        for item in data["results"]:
            yield item

    def _clean_dict(self, data: dict) -> dict:
        data.pop("info")
        return data

    def write(self, data: dict) -> None:
        for line in self._subdicts_into_dict(self._clean_dict(data)):
            self._write_line(line)

class S3Writer(DataWriter):
    def __init__(self, api: str) -> None:
        super().__init__(api)

        self.s3 = boto3.resource('s3')
        
    
    def _read_file(self):
        with open(file=self.filename,mode='rb') as file:
            return file.read()
    
    def write(self, data: dict) -> None:
        super().write(data)
        self.write_to_s3('miyamoto-datalake-raw')
    
    def write_to_s3(self,bucket: str):
        data = self._read_file()
        self.s3.Bucket(bucket).put_object(Key=self.filename,Body='data')



        
