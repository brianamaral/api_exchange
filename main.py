from ingestors import UserFetchIngestor
from writers import DataWriter
import datetime
import time
from schedule import every, repeat, run_pending

if __name__ == "__main__":

    ingestor = UserFetchIngestor(writer=DataWriter)

    @repeat(every(1).seconds)
    def job():
        ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
