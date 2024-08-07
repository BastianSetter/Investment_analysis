import numpy as np
from datetime import date
from abc import ABC, abstractmethod

from triggers import Trigger

class Depositer(ABC):
    def __init__(self) -> None:
        self.triggers = []

    def add_trigger(self, trigger:Trigger):
        self.triggers.append(trigger)

    def deposit(self, date, portfolio):
        rebalance_today = any(trigger.check_trigger(date, portfolio) for trigger in self.triggers)                

        if not rebalance_today: return 

        self.execute_deposit(date, portfolio)
    
    @abstractmethod
    def execute_deposit(self, date, portfolio):
        ...

class PureCash(Depositer):
    def __init__(self, deposit_value) -> None:
        super().__init__()
        
        self.cash_deposit_value = deposit_value
        
    
    def execute_deposit(self, date, portfolio):
        portfolio.cash_position += self.cash_deposit_value
        

class DistributedCash(Depositer):
    def __init__(self, deposit_value) -> None:
        super().__init__()
        
        self.cash_deposit_value = deposit_value
        
    
    def execute_deposit(self, date, portfolio):
        portfolio.cash_position += self.cash_deposit_value
        #TODO:redo
        portfolio.rebalancer.buy_under_positions(date, self)

class FixedShare(Depositer):
    def __init__(self, deposit_value, asset_key) -> None:
        super().__init__()
        
        self.cash_deposit_value = deposit_value
        self.asset_key = asset_key
        #TODO: use asset directly
        
    
    def execute_deposit(self, date, portfolio):
        
        asset = portfolio.find_asset_by_key(self.asset_key)
        buy_order = asset.buy_per_value(self.cash_deposit_value, date)
        portfolio.combined_order_history.append(buy_order)

class DynamicShare(Depositer):
    ...