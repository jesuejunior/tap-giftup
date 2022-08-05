import requests


class GiftupClient:

    def __init__(self, config):
        self.base_url = "https://api.giftup.app"
        self.config = config


    def __request_transaction(self, request_params):
        url = self.base_url + "/reports/transactions"
        return requests.get(
            url, 
            headers={"Authorization": "Bearer " + self.config["token"]},
            params=request_params)


    def __get_transactions_while_has_more(self, request_params, transactions, has_more):
        while has_more:
            request_params["offset"] += request_params["limit"]
            
            more_result = (self
                .__request_transaction(request_params) 
                .json())

            transactions += more_result["transactions"]
            has_more = more_result["hasMore"]
        
        return transactions


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

        return self.__get_transactions_while_has_more(request_params, transactions, has_more)

