from typing import Dict, Optional

from tap_giftup.streams.base import GiftupBaseStream


class CompanyStream(GiftupBaseStream):
    STREAM_NAME = "company"
    KEY_PROP = "id"

    def make_request(self, endpoint: Optional[str] = None, params: Optional[Dict[str, str]] = None):
        res = self.giftup_client.get_company()
        return [res]

