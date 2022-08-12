#!/usr/bin/env python3
import os
import singer

from singer import utils as singer_utils
from tap_giftup.runner import TapGiftupRunner


REQUIRED_CONFIG_KEYS = ["start_date", "auth_token"]
LOGGER = singer.get_logger()



## TODO: create schemas for the listed endpoints

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


@singer_utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)

    runner = TapGiftupRunner(args.config, args.state)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = runner.discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = runner.discover()
        runner.sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
