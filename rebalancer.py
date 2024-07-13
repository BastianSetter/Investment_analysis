import numpy as np
from datetime import date
from abc import ABC, abstractmethod
from enum import Enum

class RebalanceTrigger(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    #TODO correct stat input
    def check_for_rebalance(self, date:date, daily_stats):
        ...



class TimeUnit(Enum):
    DAYS = 'days'
    WEEKS = 'weeks'
    MONTHS = 'months'
    YEARS = 'years'

class TimeTrigger(RebalanceTrigger):
    def __init__(self, time_unit: TimeUnit = TimeUnit.MONTHS, time_interval: int = 6, reference_date: date = date(2024,1,7)) -> None:
        self.time_unit = time_unit
        self.time_interval = time_interval
        self.reference_date = reference_date

    def check_for_rebalance(self, date: date, daily_stats) -> bool:
        
        match self.time_unit:
            case TimeUnit.DAYS:
                delta_days = (date - self.reference_date).days
                return delta_days % self.time_interval == 0
        
            case TimeUnit.WEEKS:
                delta_weeks = (date - self.reference_date).days / 7
                return delta_weeks % self.time_interval == 0
    
            case TimeUnit.MONTHS:
                if date.day != self.reference_date.day:
                    return False
                
                delta_months = (date.year - self.reference_date.year) * 12 + (date.month - self.reference_date.month)
                return delta_months % self.time_interval == 0

            case TimeUnit.YEARS:
                if date.day != self.reference_date.day:
                    return False
                if date.month != self.reference_date.month:
                    return False
                
                delta_years = date.year - self.reference_date.year
                return delta_years % self.time_interval == 0



class DeviationTrigger(RebalanceTrigger):
    def __init__(self) -> None:
        super().__init__()