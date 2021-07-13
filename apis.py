import datetime
import requests
import json
import backoff
import logging
from datetime import date
import os
from abc import ABC, abstractmethod

logging.basicConfig(format='%(asctime)s %(message)s',datefmt="%d-%m-%Y %H-%M-%S",level=logging.INFO)

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

    
        response = f"{self.base_url}/?results={n_results}&nat=br"

        logging.info(f'Getting response from {response}')
        return response



