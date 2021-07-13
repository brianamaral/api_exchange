import datetime
import requests
import json
from datetime import date
import os
from abc import ABC, abstractmethod


class BaseApi(ABC):
    def __init__(self) -> None:
        self.base_url = "https://randomuser.me/api"

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    def get_response(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)

        request = requests.get(endpoint)

        return request.json()


class UserFetchApi(BaseApi):
    type = "users_events"

    def _get_endpoint(self, n_results: int = 10) -> str:
        return f"{self.base_url}/?results={n_results}&nat=br"


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


class DataIngestor(ABC):
    def __init__(self, writer) -> None:
        self.writer = writer

    @abstractmethod
    def ingest(self) -> None:
        pass


class UserFetchIngestor(DataIngestor):
    def ingest(self) -> None:

        api = UserFetchApi()
        data = api.get_response(n_results=50)
        writer = self.writer(api=api.type)
        writer.write(data=data)
