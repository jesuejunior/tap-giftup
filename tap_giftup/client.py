import requests

# DONE: reports, Gifts cards, items, users, companies
# TODO: orders

class GiftupClient:

    def __init__(self, config):
        self.base_url = "https://api.giftup.app"
        self.config = config


    def __make_request(self, url, params={}):
        return requests.get(
            url, 
            headers={"Authorization": "Bearer " + self.config["token"]},
            params=params)

    
    def __request_transaction(self, request_params):
        return self.__make_request(f"{self.base_url}/reports/transactions", request_params)

    
    def __request_gift_cards(self, request_params):
        return self.__make_request(f"{self.base_url}/gift-cards", request_params)

    
    def __request_items(self):
        return self.__make_request(f"{self.base_url}/items")

    
    def __get_users(self):
        return self.__make_request(f"{self.base_url}/users")

    
    def __get_company(self):
        return self.__make_request(f"{self.base_url}/company")

    
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

        response = self.__request_transaction(request_params)
        result = response.json()
        has_more = result["hasMore"]
        transactions += result["transactions"]

        return self.__get_resources_while_has_more(
            request_params=request_params,
            resources=transactions,
            has_more=has_more,
            resource_name="transactions",
            request_action=self.__request_transaction
        )

    
    def get_gift_cards(self, start_date, end_date, limit=100, offset=0):
        gift_cards = []
        request_params = {
            "eventOccurredOnOrAfter": start_date,
            "eventOccurredOnOrBefore": end_date,
            "limit": limit,
            "offset": offset
        }

        response = self.__request_gift_cards(request_params)
        result = response.json()
        has_more = result["hasMore"]
        gift_cards += result["giftCards"]        

        return self.__get_resources_while_has_more(
            request_params=request_params,
            resources=gift_cards,
            has_more=has_more,
            resource_name="giftCards",
            request_action=self.__request_gift_cards
        )


    def get_items(self):
        return self.__request_items().json()

    
    def get_users(self):
        return self.__get_users().json()


    def get_company(self):
        return self.__get_company().json()


