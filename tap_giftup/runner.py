import os
import json
from typing import Dict
import singer
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from tap_giftup.streams import AVAILABLE_STREAMS
from tap_giftup.utils import get_abs_path
from tap_giftup.client import GiftupClient


LOGGER = singer.get_logger()


class TapGiftupRunner:

    def __init__(self, config, state):
        self.config: Dict[str, str] = config
        self.state: Dict[str, str] = state
        self.giftup_client: GiftupClient = GiftupClient(self.config, self.state)
        self.streams = [Stream(config, state, self.giftup_client) for Stream in AVAILABLE_STREAMS]


    def discover(self):
        raw_schemas = self.load_schemas()
        streams = []
        for stream_id, schema in raw_schemas.items():
            stream_metadata = []
            key_properties = []
            streams.append(
                CatalogEntry(
                    tap_stream_id=stream_id,
                    stream=stream_id,
                    schema=schema,
                    key_properties=key_properties,
                    metadata=stream_metadata,
                    replication_key=None,
                    is_view=None,
                    database=None,
                    table=None,
                    row_count=None,
                    stream_alias=None,
                    replication_method=None,
                )
            )
        return Catalog(streams)


    def load_schemas(self):
        """ Load schemas from schemas folder """
        schemas = {}
        for filename in os.listdir(get_abs_path("schemas")):
            path = get_abs_path("schemas") + "/" + filename
            file_raw = filename.replace(".json", "")
            with open(path) as file:
                content = json.load(file)
                # schemas[file_raw] = Schema.from_dict(content)
                schemas[file_raw] = content
        return schemas


    def sync(self):
        """
        Sync data from tap source
        """
        LOGGER.info("Starting sync")

        schemas = self.load_schemas()

        for stream in self.streams:
            stream.set_schema(schemas.get(stream.STREAM_NAME))
            
            if stream.STREAM_NAME == "gift_cards":
                stream.sync()

        return
