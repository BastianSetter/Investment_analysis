from data.file_loading import DATE_FORMAT, load_data
from datetime import datetime
import numpy as np

def get_investment_length(buy_date:str, sell_date:str):
        a = datetime.strptime(buy_date, DATE_FORMAT)
        b = datetime.strptime(sell_date, DATE_FORMAT)
        delta = b - a
        return delta.days

class Investment():
    def __init__(self, key:str, ratio:float) -> None:
        self.dates, self.price = load_data(key)
        self.total_amount = 0
        self.target_ratio = ratio

    def get_price_from_date(self, date:str) -> float:
        index = np.argwhere(self.dates==date)[0][0]
        price = self.price[index]
        return price
    
    def get_roi(self, buy_date:str, sell_date:str):
        buy_price = self.get_price_from_date(buy_date)
        sell_price = self.get_price_from_date(sell_date)
        roi = sell_price/buy_price - 1 
        return roi
    
    def calculate_sell_cost():
        ...
    
    def calculate_buy_cost():
        ...

    def calculate_hold_cost():
        ...


class Share(Investment):
    def __init__(self, key: str) -> None:
        super().__init__(key)


