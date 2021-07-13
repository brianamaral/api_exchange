import os 
import datetime
import json

class DataWriter:
    def __init__(self, api: str) -> None:
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