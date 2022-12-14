from datetime import timedelta
from dateutil import parser as date_parser
from typing import Dict, Optional
import singer
from tap_giftup import utils
from tap_giftup.client import GiftupClient
from tap_giftup.utils import KeyPropNotSetError, SchemaNotSetError
from singer.schema import Schema


LOGGER = singer.get_logger()

class GiftupBaseStream:
    """
    Stream base class
    """

    STREAM_NAME = ""
    ENDOINT = ""
    KEY_PROP = ""
    IS_KEY_PROP_DATE = False

    def __init__(self, config, state, giftup_client):
        self.schema: Optional[Schema] = None
        self.config: Dict[str, str] = config
        self.state: Dict[str, str] = state
        self.giftup_client: GiftupClient = giftup_client
        self.last_record: str = state.get("last_record", config.get("start_date", ""))

        self.bookmark_date = singer.get_bookmark(
            state=state, 
            tap_stream_id=self.STREAM_NAME, 
            key="last_record"
        )

        if not self.bookmark_date:
            self.bookmark_date = self.state.get(
                "last_record", 
                self.config.get("start_date", "")
            )
        
        if self.KEY_PROP == "":
            raise KeyPropNotSetError()

    
    def set_schema(self, schema):
        self.schema = schema


    def make_request(self, endpoint: Optional[str]=None, params:Optional[Dict[str, str]]=None):
        if endpoint is None:
            endpoint = self.ENDOINT

        if params is None:
            params = {}
        
        return self.giftup_client.make_request(endpoint=endpoint, params=params)


    def sync(self):
        if not self.schema:
            raise SchemaNotSetError()

        singer.write_schema(self.STREAM_NAME,  self.schema, self.KEY_PROP)
        self.do_sync()
        singer.write_state(self.state)


    def add_one_day_to_date(self, date_str: str):
        p = date_parser.parser()
        new_date = p.parse(timestr=date_str) - timedelta(days=1)
        return new_date.strftime("%Y-%m-%dT%H:%M:%S.%s")


    def do_sync(self):
        """
        Sync data from tap source
        """
        response = self.make_request()

        old_bookmark_date = self.bookmark_date
        new_bookmark_date = self.bookmark_date
        
        LOGGER.info(f"Start bookmark: {new_bookmark_date}")
        with singer.metrics.Counter("record_count", {"endpoint": self.STREAM_NAME}) as counter:
            for row in response:
                if self.IS_KEY_PROP_DATE:
                    new_bookmark_date = row.get(self.KEY_PROP)
                elif old_bookmark_date == new_bookmark_date:
                    new_bookmark_date = self.add_one_day_to_date(self.bookmark_date) 
                    
                singer.write_message(singer.RecordMessage(
                    stream=self.STREAM_NAME,
                    record=row
                ))

            counter.increment()
        self.state = singer.write_bookmark(self.state, self.STREAM_NAME, "last_record", new_bookmark_date)
        LOGGER.warning(f"state: {self.state}")

