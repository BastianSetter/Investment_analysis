from datetime import date
from abc import ABC, abstractmethod
from enum import Enum, auto
from propagation import Portfolio
from investmentclasses import Investment



class Trigger(ABC):
    #TODO only weekdays bool
    #TODO enforce types
    @abstractmethod
    def check_trigger():
        ...

class TimeUnit(Enum):
    DAYS = auto()
    WEEKS = auto()
    MONTHS = auto()
    YEARS = auto()

class TimeTrigger(Trigger):
    def __init__(self, time_unit: TimeUnit = TimeUnit.MONTHS, time_interval: int = 6, reference_date: date = date(2024,1,7)):
        self.time_unit = time_unit
        self.time_interval = time_interval
        self.reference_date = reference_date

    def check_trigger(self, date: date) -> bool:
        
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
            
class DeviationType(Enum):
    ABSOLUTE = auto()
    RELATIVE = auto()

class DeviationTrigger(Trigger):
    def __init__(self, deviation_type: DeviationType, deviation_threshold: float, include_cash:bool = True):
        self.deviation_type = deviation_type
        self.deviation_threshold = deviation_threshold
        self.include_cash = include_cash

    def check_trigger(self, date:date, portfolio:Portfolio):
        #get_target_values
        total_portfolio_value = portfolio.calculate_total_value(date, self.include_cash)

        asset:Investment
        for asset in portfolio.assets:
            asset_value = asset.get_price_from_date(date) * asset.total_amount
            actual_ratio = asset_value/total_portfolio_value
            match self.deviation_type:
                case DeviationType.ABSOLUTE:
                    deviation = actual_ratio - asset.target_ratio
                case DeviationType.RELATIVE:
                    deviation = actual_ratio / asset.target_ratio
            if abs(deviation) > self.deviation_threshold:
                return True
        
        return False
