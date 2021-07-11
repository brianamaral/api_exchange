import requests
from datetime import date
from abc import ABC, abstractmethod

class BaseExcangeRateApi(ABC):
    def __init__(self, base_coin: str,symbols: str = 'USD,EUR,BTC',places: int = 2) -> None:
        self.base_url = 'https://api.exchangerate.host'
        self.base_coin = base_coin
        self.symbols = symbols
        self.places = places

    @abstractmethod
    def _get_endpoint(self,**kwargs) -> str:
        pass

    def get_response(self,**kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)

        request = requests.get(endpoint)

        return request.json()

class HistoricalRateApi(BaseExcangeRateApi):
    def _get_endpoint(self, ex_date: date) -> str:
        if ex_date > date.today():
            raise RuntimeError('the requested date cannot be greater than today')
        else:
            return f'{self.base_url}/{ex_date}?base={self.base_coin}&symbols={self.symbols}&places={self.places}'
        
