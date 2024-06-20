from data.file_loading import DATE_FORMAT
from datetime import datetime
import numpy as np

def get_investment_length(buy_date:str, sell_date:str):
        a = datetime.strptime(buy_date, DATE_FORMAT)
        b = datetime.strptime(sell_date, DATE_FORMAT)
        delta = b - a
        return delta.days

class Investment():
    def __init__(self, investent_price_history:np.ndarray) -> None:
        self.price = investent_price_history[0,:]
        self.dates = investent_price_history[1,:]

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
        pass
    
    def calculate_buy_cost():
        pass

    def calculate_hold_cost():
        pass


class Share(Investment):
    def __init__(self, share_price_history) -> None:
        super().__init__()


