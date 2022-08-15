import requests

from tap_giftup.utils import convert_dict_keys_to_snake

# DONE: reports, Gifts cards, items, users, companies
# TODO: orders

class GiftupClient:

    def __init__(self, config, state):
        self.base_url = "https://api.giftup.app"
        self.config = config
        self.state = state


    def make_request(self, endpoint, params={}):
        return requests.get(
            f"{self.base_url}{endpoint}", 
            headers={"Authorization": "Bearer " + self.config.get("auth_token", "")},
            params=params)

    
    def __get_resources_while_has_more(self, request_params, resources, has_more, resource_name, request_action):
        while has_more:
            request_params["offset"] += request_params["limit"]
            more_result = request_action(request_params).json()
            resources += more_result[resource_name]
            has_more = more_result["hasMore"]
        
        return resources

    
    def get_reports(self, start_date, end_date, limit=100, offset=0):
        transactions = []
        request_params = {
            "eventOccurredOnOrAfter": start_date,
            "eventOccurredOnOrBefore": end_date,
            "limit": limit,
            "offset": offset
        }

        request_transactions = lambda params: self.make_request(
            "/reports/transactions", 
            params
        )

        response = request_transactions(request_params)
        result = response.json()
        has_more = result.get("hasMore", False)
        transactions += result["transactions"]

        res = self.__get_resources_while_has_more(
            request_params=request_params,
            resources=transactions,
            has_more=has_more,
            resource_name="transactions",
            request_action=request_transactions
        )

        return convert_dict_keys_to_snake(res)

    
    def get_gift_cards(self, start_date, end_date, limit=100, offset=0):
        gift_cards = []
        request_params = {
            "eventOccurredOnOrAfter": start_date,
            "eventOccurredOnOrBefore": end_date,
            "limit": limit,
            "offset": offset
        }

        request_gift_cards = lambda params: self.make_request(
            "/gift-cards", 
            params
        )

        response = request_gift_cards(request_params)
        result = response.json()
        has_more = result["hasMore"]
        gift_cards += result["giftCards"]        

        res = self.__get_resources_while_has_more(
            request_params=request_params,
            resources=gift_cards,
            has_more=has_more,
            resource_name="giftCards",
            request_action=request_gift_cards
        )

        return convert_dict_keys_to_snake(res)


    def get_items(self):
        return convert_dict_keys_to_snake(self.make_request("/items").json()) 

    
    def get_users(self):
        return convert_dict_keys_to_snake(self.make_request("/users").json()) 


    def get_company(self):
        return convert_dict_keys_to_snake(self.make_request("/company").json()) 


