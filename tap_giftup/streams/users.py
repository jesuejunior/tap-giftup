from typing import Dict, Optional

from tap_giftup.streams.base import GiftupBaseStream


class UserStream(GiftupBaseStream):
    STREAM_NAME = "users"
    KEY_PROP = "id"

    def make_request(self, endpoint: Optional[str] = None, params: Optional[Dict[str, str]] = None):
        return self.giftup_client.get_users()

