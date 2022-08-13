#!/usr/bin/env python3
import os
import singer

from singer import utils as singer_utils
from tap_giftup.runner import TapGiftupRunner


REQUIRED_CONFIG_KEYS = ["start_date", "auth_token"]
LOGGER = singer.get_logger()


@singer_utils.handle_top_exception(LOGGER)
def main():
    args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)
    runner = TapGiftupRunner(args.config, args.state)
    
    if args.discover:
        catalog = runner.discover()
        catalog.dump()
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = runner.discover()
        runner.sync()


if __name__ == "__main__":
    main()
