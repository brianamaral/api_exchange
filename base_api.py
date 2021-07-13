import datetime
import requests
import json
from datetime import date
import os
from abc import ABC, abstractmethod


class BaseExcangeRateApi(ABC):
    def __init__(self, base_coin: str = 'USD',symbols: str = 'USD,EUR,BTC',places: int = 2) -> None:
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
    type = "historical"
    def _get_endpoint(self, ex_date: date) -> str:
        if ex_date > date.today():
            raise RuntimeError('the requested date cannot be greater than today')
        else:
            return f'{self.base_url}/{ex_date}?base={self.base_coin}&symbols={self.symbols}&places={self.places}'
        
class TimeSeriesApi(BaseExcangeRateApi):
    type = "timeseries"
    def _get_endpoint(self, start_date: date, end_date: date) -> str:
        if start_date > end_date:
            raise RuntimeError(f'start_date cannot be greater than end_date {start_date} > {end_date}')
        elif end_date > date.today():
            raise RuntimeError(f'end_date cannot be greater than today {end_date}')
        else:
            return f'{self.base_url}/timeseries?start_date={start_date}&end_date={end_date}&base={self.base_coin}&symbols={self.symbols}&places={self.places}'

class DataWriter():
    def __init__(self,base: str,api: str) -> None:
        self.base = base
        self.api = api
        self.filename = f'{api}/{base}/{date.today()}.json'
        self.file = self._open_file(self.filename)
            

    def _open_file(self,file):
        os.makedirs(os.path.dirname(self.filename),exist_ok=True)
        return open(file = file,mode='a')
    
    def _write_line(self,line: str) -> None:
        self.file.write(json.dumps(line) + '\n')

    def _subdicts_into_dict(self,data: dict) -> iter:
        for item,value in data['rates'].items():
            new_dict = {}
            date = item
            new_dict['base'] = data['base']
            new_dict['date'] = date
            new_dict['rates'] = value

            yield new_dict
    
    def _clean_dict(self,data: dict) -> dict:
        
        data.pop('motd')
        data.pop('success')
        data.pop('historical')

        return data    
    
    def write(self,data: dict) -> None:
        if 'timeseries' in data.keys():
            for line in self._subdicts_into_dict(data):
                self._write_line(line)
        else:
            self._write_line(self._clean_dict(data))

class DataIngestor(ABC):
    def __init__(self,writer, bases: list[str], default_start_date: date,symbols:str = 'BTC,USD,EUR') -> None:
        self.default_start_date = default_start_date
        self.bases = bases
        self.writer = writer
        self.symbols = symbols
    
    @abstractmethod
    def ingest(self) -> None:
        pass

class TimeSeriesIngestor(DataIngestor):
    def ingest(self) -> None:
        for base in self.bases:
            api = TimeSeriesApi(base_coin=base,places=5,symbols=self.symbols)
            data = api.get_response(start_date = self.default_start_date,end_date = date.today())
            writer = self.writer(base = base,api = api.type)
            writer.write(data = data)



