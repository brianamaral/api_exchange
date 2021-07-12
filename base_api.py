import datetime
import requests
import json
from datetime import date
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
    def _get_endpoint(self, ex_date: date) -> str:
        if ex_date > date.today():
            raise RuntimeError('the requested date cannot be greater than today')
        else:
            return f'{self.base_url}/{ex_date}?base={self.base_coin}&symbols={self.symbols}&places={self.places}'
        
class TimeSeriesApi(BaseExcangeRateApi):
    def _get_endpoint(self, start_date: date, end_date: date) -> str:
        if start_date > end_date:
            raise RuntimeError(f'start_date cannot be greater than end_date {start_date} > {end_date}')
        elif end_date > date.today():
            raise RuntimeError(f'end_date cannot be greater than today {end_date}')
        else:
            return f'{self.base_url}/timeseries?start_date={start_date}&end_date={end_date}&base={self.base_coin}&symbols={self.symbols}&places={self.places}'

class DataWriter():
    def __init__(self,filename: str,mode: str = "a") -> None:
        if mode == 'r':
            raise RuntimeError('Cannot open file in read mode')
        else:
            self.mode = mode
            self.file = self._open_file(filename)
            

    def _open_file(self,file):
        
        return open(file = file,mode=self.mode)
    
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


        
