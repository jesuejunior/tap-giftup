from tap_giftup.streams.company import CompanyStream
from tap_giftup.streams.gift_cards import GiftCardsStream
from tap_giftup.streams.items import ItemsStream
from tap_giftup.streams.users import UserStream
from tap_giftup.streams.transactions import TransactionStream

AVAILABLE_STREAMS = (
    CompanyStream,
    GiftCardsStream,
    ItemsStream,
    TransactionStream,
    UserStream,
)
