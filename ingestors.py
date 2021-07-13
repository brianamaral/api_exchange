from abc import ABC, abstractmethod
from apis import UserFetchApi

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