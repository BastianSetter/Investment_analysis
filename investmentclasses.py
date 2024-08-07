from data.file_loading import load_data
from datetime import datetime
from dataclasses import dataclass
from collections import deque
import numpy as np
from abc import ABC, abstractmethod


@dataclass
class HistoryOrder:
    key_name: str
    date: datetime
    amount: float
    order_price: float
    fees: float
    tax: float

@dataclass
class OngoiningOrder:
    date: datetime
    remaining_amount: float
    order_price: float

def get_hold_time(buy_date:datetime, sell_date:datetime):
    delta = sell_date - buy_date
    return delta.days

class Investment(ABC):
    def __init__(self, key:str, ratio:float, ongoing_cost:float = 0) -> None:
        self.dates, self.price = load_data(key)
        self.total_amount = 0
        self.target_ratio = ratio
        self.open_orders = deque([])

        self.capital_gains_tax = 0.25
        self.key_name = key

    def get_price_from_date(self, date:datetime) -> float:
        index = np.argwhere(self.dates==date)[0][0]
        price = self.price[index]
        return price
    
    def get_roi(self, buy_date:str, sell_date:str):
        buy_price = self.get_price_from_date(buy_date)
        sell_price = self.get_price_from_date(sell_date)
        roi = sell_price/buy_price - 1
        return roi
    
    def rebalance_amount(self, total_portfolio_value, date):
        asset_price = self.get_price_from_date(date)
        asset_value = asset_price * self.total_amount
        target_value = total_portfolio_value * self.target_ratio
        value_diff = asset_value-target_value
        return value_diff/asset_price 

    def sell_amount(self, amount, date):
        remaining_amount = amount
        combined_tax = 0
        sell_price = self.get_price_from_date(date)
        combined_fee = self.calculate_sell_fee(sell_price * amount)

        while remaining_amount > 0:
            first_order = self.open_orders[0]
            if remaining_amount > first_order.remaining_amount:
                sell_amount = first_order.remaining_amount
                self.open_orders.popleft()

            else:
                sell_amount = remaining_amount
                first_order.remaining_amount -= remaining_amount

            remaining_amount -= sell_amount
            combined_tax += self.calculate_sell_tax(first_order.order_price, sell_price, sell_amount)
        
        self.total_amount -= amount
        sell_order = HistoryOrder(self.key_name, date, amount, sell_price, combined_fee, combined_tax)
        return sell_order
    
    def buy_per_piece(self, amount, date):
        buy_price = self.get_price_from_date(date)
        cash_estimate = buy_price*amount
        fee_estimate = self.calculate_buy_fee(cash_estimate)
        final_amount = (cash_estimate-fee_estimate)/buy_price
        self.total_amount += final_amount

        open_order = OngoiningOrder(date, final_amount, buy_price)
        self.open_orders.append(open_order)

        buy_order = HistoryOrder(self.key_name, date, final_amount, buy_price, fee_estimate, 0)
        return buy_order
    
    def buy_per_value(self, value, date):
        cash_estimate = value
        buy_price = self.get_price_from_date(date)
        fee_estimate = self.calculate_buy_fee(cash_estimate)
        final_amount = (cash_estimate-fee_estimate)/buy_price
        self.total_amount += final_amount

        open_order = OngoiningOrder(date, final_amount, buy_price)
        self.open_orders.append(open_order)

        buy_order = HistoryOrder(self.key_name, date, final_amount, buy_price, fee_estimate, 0)
        return buy_order

    @abstractmethod
    def calculate_sell_tax(self, buy_price, sell_price, amount)-> float:
        ...

    @abstractmethod
    def calculate_sell_fee(self, sell_value)-> float:
        ...

    @abstractmethod
    def calculate_buy_fee(self, buy_value)-> float:
        ...

    # @abstractmethod
    # def calculate_hold_cost():
    #     ...


class Share(Investment):
    def __init__(self, key: str, ratio:float) -> None:
        super().__init__(key, ratio)
        self.flat_buy_price = 1

    def calculate_sell_tax(self, buy_price, sell_price, amount) -> float:
        gains = (sell_price - buy_price) * amount
        return gains*self.capital_gains_tax
    
    def calculate_sell_fee(self, sell_value) -> float:
        return 0
    
    def calculate_buy_fee(self, buy_value) -> float:
        return self.flat_buy_price