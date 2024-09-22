import numpy as np
from datetime import date
from abc import ABC, abstractmethod
#typehinting
import triggers
import propagation

class Depositer(ABC):
    def __init__(self) -> None:
        self.triggers = []

    def add_trigger(self, trigger:'triggers.Trigger'):
        self.triggers.append(trigger)

    def deposit(self, date:date, portfolio:'propagation.Portfolio'):
        rebalance_today = any(trigger.check_trigger(date, portfolio) for trigger in self.triggers)
        if not rebalance_today: return 

        self.execute_deposit(date, portfolio)
    
    @abstractmethod
    def execute_deposit(self, date:date, portfolio:'propagation.Portfolio'):
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
        portfolio.rebalancer.execute_rebalance(date, portfolio)

class FixedShare(Depositer):
    def __init__(self, deposit_value, asset) -> None:
        super().__init__()
        
        self.cash_deposit_value = deposit_value
        self.asset = asset        
    
    def execute_deposit(self, date, portfolio):
        
        buy_order = self.asset.buy_per_value(self.cash_deposit_value, date)
        portfolio.combined_order_history.append(buy_order)

class DynamicShare(Depositer):
    ...
    #idea:
    # self.valid_plan_sizes
    # self.self.cash_deposit_value = deposit_value