from ingestors import UserFetchIngestor
from writers import DataWriter,S3Writer
import datetime
import time
from schedule import every, repeat, run_pending

if __name__ == "__main__":

    ingestor = UserFetchIngestor(writer=S3Writer)

    @repeat(every(1).minutes)
    def job():
        ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
