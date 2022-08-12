import requests

# DONE: reports, Gifts cards, items, users, companies
# TODO: orders

class GiftupClient:

    def __init__(self, config, state):
        self.base_url = "https://api.giftup.app"
        self.config = config
        self.state = state


    def make_request(self, url, params={}):
        return requests.get(
            url, 
            headers={"Authorization": "Bearer " + self.config.get("token")},
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
            f"{self.base_url}/reports/transactions", 
            params
        )

        response = request_transactions(request_params)
        result = response.json()
        has_more = result["hasMore"]
        transactions += result["transactions"]

        return self.__get_resources_while_has_more(
            request_params=request_params,
            resources=transactions,
            has_more=has_more,
            resource_name="transactions",
            request_action=request_transactions
        )

    
    def get_gift_cards(self, start_date, end_date, limit=100, offset=0):
        gift_cards = []
        request_params = {
            "eventOccurredOnOrAfter": start_date,
            "eventOccurredOnOrBefore": end_date,
            "limit": limit,
            "offset": offset
        }

        request_gift_cards = lambda params: self.make_request(
            f"{self.base_url}/gift-cards", 
            params
        )

        response = request_gift_cards(request_params)
        result = response.json()
        has_more = result["hasMore"]
        gift_cards += result["giftCards"]        

        return self.__get_resources_while_has_more(
            request_params=request_params,
            resources=gift_cards,
            has_more=has_more,
            resource_name="giftCards",
            request_action=request_gift_cards
        )


    def get_items(self):
        return self.make_request(f"{self.base_url}/items").json()

    
    def get_users(self):
        return self.make_request(f"{self.base_url}/users").json()


    def get_company(self):
        return self.make_request(f"{self.base_url}/company").json()


