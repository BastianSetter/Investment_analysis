from data.file_loading import load_data
from datetime import date
from dataclasses import dataclass
from collections import deque
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from icecream import ic


@dataclass
class HistoryOrder:
    key_name: str
    date: date
    amount: float
    order_price: float
    fees: float
    tax: float

@dataclass
class OngoiningOrder:
    date: date
    remaining_amount: float
    order_price: float

# def get_hold_time(buy_date:date, sell_date:date):
#     delta = sell_date - buy_date
#     return delta.days

#Default cost settings
FLAT_HOLD = 0
PERCENT_HOLD = 0
FLAT_BUY = 1
PERCENT_BUY = 0
FLAT_SELL = 1
PERCENT_SELL_FEE = 0
PERCENT_SELL_TAX = 0.25

class Investment(ABC):
    def __init__(self, key:str, ratio:float, 
                flat_hold = FLAT_HOLD, percent_hold = PERCENT_HOLD, flat_buy = FLAT_BUY, percent_buy = PERCENT_BUY,
                flat_sell = FLAT_SELL, percent_sell_fee = PERCENT_SELL_FEE, percent_sell_tax = PERCENT_SELL_TAX
                ) -> None:
        self.dates, self.price = load_data(key)
        self.total_amount = 0
        self.target_ratio = ratio
        self.open_orders = deque([])

        self.flat_hold_fee_per_year = flat_hold
        self.precent_hold_fee_per_year = percent_hold
        self.flat_buy_fee = flat_buy
        self.percent_buy_fee = percent_buy
        self.flat_sell_fee = flat_sell
        self.percent_sell_fee = percent_sell_fee

        self.percent_sell_tax = percent_sell_tax
        #TODO: exempt after timeperiod

        self.cost_function_table = pd.DataFrame(data = [[0,np.inf,0,0]], columns=['lower_bound', 'upper_bound', 'slope', 'starting_value'])
        self.key_name = key

    def get_price_from_date(self, date:date) -> float:
        index = np.argwhere(self.dates==date)[0][0]
        price = self.price[index]
        return price
    
    def get_current_value(self, date:date):
        return self.total_amount * self.get_price_from_date(date)

    def get_roi(self, buy_date:str, sell_date:str):
        buy_price = self.get_price_from_date(buy_date)
        sell_price = self.get_price_from_date(sell_date)
        roi = sell_price/buy_price - 1
        return roi
    
    def rebalance_amount(self, total_portfolio_value:float, date:date):
        asset_price = self.get_price_from_date(date)
        asset_value = asset_price * self.total_amount
        target_value = total_portfolio_value * self.target_ratio
        value_diff = asset_value-target_value
        return value_diff/asset_price 

    def cost_function(self, value:float) -> float:
        up_mask = self.cost_function_table['upper_bound']>value
        low_mask = self.cost_function_table['lower_bound']<=value
        relevant_row = self.cost_function_table[(up_mask)&(low_mask)]
        assert len(relevant_row) == 1

        cost = relevant_row['starting_value']+relevant_row['slope']*(value-relevant_row['lower_bound'])
        return cost.item()

    def update_cost_function_table(self, date:date):
        cur_price = self.get_price_from_date(date)
        self.cost_function_table = tab = pd.DataFrame(data = np.zeros((len(self.open_orders)+1,4)), columns=['lower_bound', 'upper_bound', 'slope', 'starting_value'])
        #insert buy costs
        tab.loc[0,'upper_bound'] = np.inf
        tab.loc[0,'lower_bound'] = 0
        tab.loc[0,'slope'] = self.percent_buy_fee
        tab.loc[0,'starting_value'] = self.flat_buy_fee

        #insert sell costs
        if len(self.open_orders)<1: return
        #first sell
        first_order = self.open_orders[0]
        tab.loc[1,'upper_bound'] = 0
        tab.loc[1,'lower_bound'] = -first_order.remaining_amount*cur_price
        tax_slope = np.max([0, self.percent_sell_tax*(1-first_order.order_price/cur_price)])
        tab.loc[1,'slope'] = -(self.percent_sell_fee+tax_slope)
        max_fees = (tab.loc[1,'lower_bound']-tab.loc[1,'upper_bound'])*tab.loc[1,'slope']
        tab.loc[1,'starting_value'] = self.flat_sell_fee+max_fees

        #further sells
        for counter, open_order in enumerate(list(self.open_orders)[1:]):
            tab.loc[2+counter,'upper_bound'] = tab.loc[1+counter,'lower_bound']
            tab.loc[2+counter,'lower_bound'] = tab.loc[1+counter,'lower_bound']-open_order.remaining_amount*cur_price
            tax_slope = np.max([0, self.percent_sell_tax*(1-first_order.order_price/cur_price)])
            tab.loc[2+counter,'slope'] = -(self.percent_sell_fee+tax_slope)
            max_fees = (tab.loc[2+counter,'lower_bound']-tab.loc[2+counter,'upper_bound'])*tab.loc[2+counter,'slope']
            tab.loc[2+counter,'starting_value'] = tab.loc[1+counter,'starting_value']+max_fees
        

    def sell_amount(self, amount:float, date:date):
        remaining_amount = -amount
        combined_tax = 0
        sell_price = self.get_price_from_date(date)
        combined_fee = self.calculate_sell_fee(sell_price * remaining_amount)

        while remaining_amount > 0:
            first_order:OngoiningOrder = self.open_orders[0]
            if remaining_amount > first_order.remaining_amount:
                sell_amount = first_order.remaining_amount
                self.open_orders.popleft()

            else:
                sell_amount = remaining_amount
                first_order.remaining_amount -= remaining_amount

            remaining_amount -= sell_amount
            sell_tax = self.calculate_sell_tax(first_order.order_price, sell_price, sell_amount)
            combined_tax += sell_tax
        
        self.total_amount -= amount
        sell_order = HistoryOrder(self.key_name, date, amount, sell_price, combined_fee, combined_tax)
        return sell_order
    
    def sell_per_value(self, value:float, date:date):
        amount = value/self.get_price_from_date(date)
        sell_order = self.sell_amount(amount, date)
        return sell_order

    def buy_per_value(self, value:float, date:date):
        buy_price = self.get_price_from_date(date)
        fees = self.calculate_buy_fee(value)
        amount = (value-fees)/buy_price
        self.total_amount += amount

        open_order = OngoiningOrder(date, amount, buy_price)
        self.open_orders.append(open_order)

        buy_order = HistoryOrder(self.key_name, date, amount, buy_price, fees, 0)
        return buy_order

    def calculate_sell_tax(self, buy_price:float, sell_price:float, amount:float) -> float:
        gains = (sell_price - buy_price) * amount
        return gains*self.percent_sell_tax
    
    def calculate_sell_fee(self, sell_value:float) -> float:
        return self.flat_sell_fee+self.percent_sell_fee*sell_value
    
    def calculate_buy_fee(self, buy_value:float) -> float:
        return self.flat_buy_fee+self.percent_buy_fee*buy_value

    # @abstractmethod
    # def calculate_hold_cost():
    #     ...

class Share(Investment):
    def __init__(self, key: str, ratio:float, **cost_settings) -> None:
        super().__init__(key, ratio, **cost_settings)

    #TODO:  adjustable cost structure and whether subclasses for different assets are the right choice
    #       Options object for cost settings

class Crypto(Investment):
    def __init__(self, key: str, ratio:float, percent_sell_tax = 0.42, **cost_settings) -> None:
        super().__init__(key, ratio, percent_sell_tax=percent_sell_tax, **cost_settings)

class Commodity(Investment):
    def __init__(self, key: str, ratio:float, percent_hold = 2, **cost_settings) -> None:
        super().__init__(key, ratio, percent_hold=percent_hold, **cost_settings)