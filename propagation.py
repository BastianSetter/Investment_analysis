import numpy as np
from data.file_loading import DATE_FORMAT
from investmentclasses import Investment
from dataclasses import dataclass
from datetime import datetime, timedelta

def generate_dates(start_date:str, end_date:str):
    start_date = datetime.strptime(start_date, DATE_FORMAT)
    end_date = datetime.strptime(end_date, DATE_FORMAT)
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

@dataclass
class Order:
    key_name: str
    buy_date = str
    buy_amount = float
    remaining_amount = float
    order_price = float
    fees = float



class Portfolio():
    def __init__(self, assets:list[Investment], rebalance_time = 0, rebalance_deviation = 0) -> None:
        total_ratio = sum(asset.ratio for asset in assets)
        assert np.isclose(total_ratio, 1)
        #TODO: renormalise
        self.assets = assets
        self.rebalance_time = rebalance_time
        self.rebalance_deviation = rebalance_deviation
        self.orders = []
        self.cash_position = 0

    def simulate_timeinterval(self, start_date, end_date):
        self.check_all_assets_in_timeinterval(start_date, end_date)
        for date in generate_dates(start_date, end_date):
            total_value = self.calculate_value(date)
            #check for rebalance
            #if yes rebalance

    def check_all_assets_in_timeinterval(self, start_date, end_date):
        ...

    def calculate_value(self, date:datetime):
        ...
