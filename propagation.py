import numpy as np
from datetime import timedelta, date
from deposits import Deposit
from investmentclasses import Commodity, Crypto, Share
from rebalancer import Rebalancer
from triggers import TimeTrigger, DeviationTrigger, DeviationType
from icecream import ic
from dataclasses import dataclass
#typehinting
import deposits
import investmentclasses
import rebalancer

# DATE_FORMAT = "%d.%m.%Y"

@dataclass
class Simulation_trace:
    stats: list
    orders: list
    deposits: list

    @property
    def internal_rate_of_return(self):
        end_date:date = self.stats[-1][0]
        final_portfolio_value = np.sum(self.stats[-1][1:])

        best_irr_approx = 0
        best_difference = np.inf
        for irr in np.linspace(0,10,10000):
            result = 0
            for deposit in self.deposits:
                invest_duration = (end_date-deposit.date).days/365.2425
                result += deposit.value*(1+irr)**invest_duration

            approx_diff = np.abs(result-final_portfolio_value)
            if approx_diff < best_difference:
                best_difference = approx_diff
                best_irr_approx = irr
            else: break

        return best_irr_approx
    
    @property
    def calculate_lost_costs(self):
        fees = 0
        taxes = 0
        for order in self.orders:
            fees += order.fees
            taxes += order.tax
        return fees + taxes
    
    # def calculate_lost_costs(self, sim_trace: 'propagation.Simulation_trace'):
    #     ...
    #     # run an additional simulation with no taxes and/or fees


def time_range(start_date:date, end_date:date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days = 1)



#TODO: reference_dates for triggers have to be set as portfolio attribute

class Portfolio():
    def __init__(self, assets:list['investmentclasses.Investment'], rebalancer:'rebalancer.Rebalancer', initial_cash:float = 0) -> None:
        total_ratio = sum(asset.target_ratio for asset in assets)
        for asset in assets:
            asset.target_ratio = asset.target_ratio/total_ratio

        self.assets = assets
        self.rebalancer = rebalancer
        self.depositers = []
        self.deposits = []
        self.combined_order_history = []
        self.portfolio_history = []
        self.initial_cash = initial_cash# TODO: part of simulation restructure
        self.cash_position = 0
    
    def add_depositer(self, depositer:'deposits.Depositer'):
        self.depositers.append(depositer)

    def simulate_timeinterval(self, start_date:date, end_date: date):
        self.assert_all_assets_valid_in_timeinterval(start_date, end_date)
        #clear previous simulations: #TODO: this should not be necesarry ==> restructure simulation responsibility. Probably into tester class.
        
        self.init_simulation(start_date)

        for date in time_range(start_date, end_date):
            #deposits
            for depositer in self.depositers:
                depositer.deposit(date, self)
                
            #TODO: ongoing costs
            #self.handle_holding_costs()

            #rebalance
            self.rebalancer.rebalance(date, self)

            #performance tracking for later visualisation
            if date is end_date:
                break
            daily_stats = self.get_daily_stats(date)
            self.portfolio_history.append(daily_stats)

        # self.sell_all(date)
        # daily_stats = self.get_daily_stats(date)
        # self.portfolio_history.append(daily_stats)
        simulation_trace = Simulation_trace(np.array(self.portfolio_history), self.combined_order_history, self.deposits)
        return simulation_trace
            
    def init_simulation(self, date):
        #TODO reset not working
        self.portfolio_history = []
        self.combined_order_history = []
        self.deposits = []

        self.cash_position = self.initial_cash
        deposit = Deposit(date, self.initial_cash)
        self.deposits.append(deposit)

    def assert_all_assets_valid_in_timeinterval(self, start_date: date, end_date: date):
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

    def find_asset_by_key(self, key: str):
        for asset in self.assets:
            if asset.key == key:
                return asset
        raise KeyError(f'"{key}" is not valid.')
    
    def get_first_common_date(self)-> date:
        earliest_date = date(0,0,0)
        for asset in self.assets:
            date = asset.dates[0] #Check order of dates in investment and place note
            if date > earliest_date:
                earliest_date = date
        return earliest_date
    
    def get_last_common_date(self) -> date:
        latest_date = date(0,0,0)
        for asset in self.assets:
            date = asset.dates[-1] #Check order of dates in investment and place note
            if date < latest_date:
                latest_date = date
        return latest_date
    
    # def handle_holding_cost(self):
    #     pass

def build_single_portfolio(blueprint: dict) -> Portfolio:
    assets = []
    for asset_bp in blueprint['asset']:
        asset_class = asset_bp.pop('class')
        asset = asset_class(**asset_bp)
        assets.append(asset)

    rebalancer = Rebalancer()
    for rebalancer_bp in blueprint['rebalancer']:
        trigger_class = rebalancer_bp.pop('class')
        trigger = trigger_class(**rebalancer_bp)
        rebalancer.add_trigger(trigger)

    portfolio = Portfolio(assets=assets, rebalancer = rebalancer, initial_cash=blueprint['initial_cash'])

    for depositer in blueprint['deposit']:
        depositer_class = asset_bp.pop('class')
        depositer = depositer_class(**asset_bp)
        portfolio.add_depositer(depositer)

    return portfolio