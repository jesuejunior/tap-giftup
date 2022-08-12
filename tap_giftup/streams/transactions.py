from dateutil import parser as date_parser
from datetime import timedelta

from tap_giftup.streams.base import GiftupBaseStream


class TransactionStream(GiftupBaseStream):
    STREAM_NAME = "transactions"

    def make_reqquest(self):
        end = date_parser.parse(self.last_record)
        start = end - timedelta(days=1)

        return self.giftup_client.get_reports(start_date=start, end_date=end)

