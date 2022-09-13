import dateutil.parser as date_parser
from datetime import datetime
import requests
from humps import main as pyhumps

# DONE: reports, Gifts cards, items, users, companies
# TODO: orders

class GiftupClient:

    def __init__(self, config, state):
        self.base_url = "https://api.giftup.app"
        self.config = config
        self.state = state


    def make_request(self, endpoint, params={}):
        return requests.get(
            url=f"{self.base_url}{endpoint}", 
            headers={"Authorization": "Bearer " + self.config.get("auth_token", "")},
            params=params)

    
    def __get_resources_while_has_more(self, request_params, resources, has_more, resource_name, request_action):
        while has_more:
            request_params["offset"] += request_params["limit"]
            more_result = request_action(request_params).json()
            resources += more_result[resource_name]
            has_more = more_result["hasMore"]
        
        return resources

    
    def __filter_by_end_date(self, gift_cards,  end_date):
        def filter_by_date(gift_card):
            dmy_date = gift_card.get("created_on").split("T")[0]
            created_date = datetime.strptime(dmy_date, '%Y-%m-%d')

            dmy_end_date = end_date.split("T")[0]
            converted_end_date = datetime.strptime(dmy_end_date, '%Y-%m-%d')

            return created_date <= converted_end_date
        
        return list(filter(filter_by_date, gift_cards))

    
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

        return pyhumps.decamelize(res)


    def get_gift_cards(self, start_date, end_date, limit=100, offset=0, res=[]):
        gift_cards = []
        request_params = {
            "createdOnOrAfter": start_date,
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

        res += self.__get_resources_while_has_more(
            request_params=request_params,
            resources=gift_cards,
            has_more=has_more,
            resource_name="giftCards",
            request_action=request_gift_cards
        )

        if end_date is not None:
            filtered = filter(lambda gc: (end_date in gc["createdOn"]), res)   
            if len(list(filtered)) == 0:
                final_iteration = self.get_gift_cards(end_date, None, limit, offset, res)
                return pyhumps.decamelize(self.__filter_by_end_date(final_iteration, end_date))

        return pyhumps.decamelize(res)


    def get_items(self):
        return pyhumps.decamelize(self.make_request("/items").json()) 

    
    def get_users(self):
        return pyhumps.decamelize(self.make_request("/users").json()) 


    def get_company(self):
        return pyhumps.decamelize(self.make_request("/company").json()) 


