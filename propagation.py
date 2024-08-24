import numpy as np
from investmentclasses import Investment
from rebalancer import Rebalancer
from deposits import Depositer
from datetime import datetime, timedelta, date

DATE_FORMAT = "%d.%m.%Y"

def time_range(start_date:str, end_date:str):
    start_date = datetime.strptime(start_date, DATE_FORMAT).date() 
    end_date = datetime.strptime(end_date, DATE_FORMAT).date() 
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


class Portfolio():
    def __init__(self, assets:list[Investment], rebalancer:Rebalancer, initial_cash = 0) -> None:#, rebalance_time = 0, rebalance_deviation = 0) -> None:
        total_ratio = sum(asset.target_ratio for asset in assets)
        assert np.isclose(total_ratio, 1)
        #TODO: renormalise
        self.assets = assets
        self.rebalancer = rebalancer
        self.depositers = []
        self.combined_order_history = []
        self.portfolio_history = []
        self.cash_position = initial_cash
    
    def add_depositer(self, depositer:Depositer):
        self.depositers.append(depositer)


    def simulate_timeinterval(self, start_date:date, end_date: date):
        self.assert_all_assets_valid_in_timeinterval(start_date, end_date)
        for date in time_range(start_date, end_date):

            #deposits
            for depositer in self.depositer:
                depositer.deposit(date, self)
                
            #TODO: ongoing costs
            #self.handle_holding_costs()

            #rebalance
            self.rebalancer.rebalance(date, self)

            #performance tracking for later visualisation
            daily_stats = self.get_daily_stats(date)
            self.portfolio_history.append(daily_stats)
            
            
            

   
            

    def assert_all_assets_valid_in_timeinterval(self, start_date, end_date):
        for asset in self.assets:
            if start_date not in asset.dates:
                raise ValueError(f'Start date "{start_date}" not in asset "{asset.key_name}"!')
            if end_date not in asset.dates:
                raise ValueError(f'End date "{start_date}" not in asset "{asset.key_name}"!')


    def calculate_total_value(self, date:date, include_cash: bool = True, changes = None):
        total_value = 0
        if changes is None:
            changes = [0]*len(self.assets)
        if include_cash:
            total_value += self.cash_position

        for asset, change in zip(self.assets, changes):
            asset_value = asset.get_current_value(date)
            cost = asset.cost_function(change)
            total_value += (asset_value - cost)
        
        return total_value

        
    def get_daily_stats(self, date: date):
        stats = [date, self.cash_position]
        for asset in self.assets:
            asset_value = asset.total_amount*asset.get_price_from_date(date)
            stats.append(asset_value)
        return np.asarray(stats)

    def find_asset_by_key(self, key):
        for asset in self.assets:
            if asset.key == key:
                return asset
        raise KeyError(f'"{key}" is not valid.')
    
    # def handle_holding_cost(self):
    #     pass