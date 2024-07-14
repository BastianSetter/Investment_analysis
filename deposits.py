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
        rebalance_today = False
        for trigger in self.triggers:
            trigger.check_trigger(date, portfolio)
        if not rebalance_today: return 

        self.execute_deposit(date, portfolio)
    
    @abstractmethod
    def execute_deposit(self, date, portfolio):
        ...

class PureCash(Depositer):
    def __init__(self, cash_deposit_value) -> None:
        super().__init__()
        
        self.cash_deposit_value = cash_deposit_value
        
    
    def execute_deposit(self, date, portfolio):
        portfolio.cash_position += self.cash_deposit_value
        

class DistributedCashPlan(Depositer):
    ...

class FixedShareSavingPlans(Depositer):
    ...

class DynamicShareSavingPlans(Depositer):
    ...