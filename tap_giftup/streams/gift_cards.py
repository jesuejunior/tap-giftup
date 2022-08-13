from typing import Dict, Optional
from dateutil import parser as date_parser, relativedelta
from datetime import datetime

from tap_giftup.streams.base import GiftupBaseStream


class GiftCardsStream(GiftupBaseStream):
    STREAM_NAME = "gift_cards"

    def make_request(self, endpoint: Optional[str] = None, params: Optional[Dict[str, str]] = None):
        end = date_parser.parse(self.last_record)
        start = end - relativedelta.relativedelta(months=1)

        start_str = datetime.strptime(start.strftime('%Y-%m-%d'), '%Y-%m-%d').strftime('%Y-%m-%d')
        end_str = datetime.strptime(end.strftime('%Y-%m-%d'), '%Y-%m-%d').strftime('%Y-%m-%d')

        return self.giftup_client.get_gift_cards(
            start_date=start_str,
            end_date=end_str)

