import numpy as np
from data.file_loading import DATE_FORMAT
from investmentclasses import Investment
from datetime import datetime, timedelta

def generate_dates(start_date:str, end_date:str):
    start_date = datetime.strptime(start_date, DATE_FORMAT)
    end_date = datetime.strptime(end_date, DATE_FORMAT)
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


class Portfolio():
    def __init__(self, assets:list[Investment]) -> None:#, rebalance_time = 0, rebalance_deviation = 0) -> None:
        total_ratio = sum(asset.ratio for asset in assets)
        assert np.isclose(total_ratio, 1)
        #TODO: renormalise
        self.assets = assets
        # self.rebalance_time = rebalance_time
        # self.rebalance_deviation = rebalance_deviation
        self.combined_order_history = []
        self.portfolio_history = []
        self.cash_position = 0

    def simulate_timeinterval(self, start_date, end_date):
        self.check_all_assets_valid_in_timeinterval(start_date, end_date)
        for date in generate_dates(start_date, end_date):

            #TODO: ongoing costs
            #self.handle_holding_costs()

            #handle periodic cash increase and buys
            if date.day == 1:
                monthly_savings = 500 #TODO: add options for this
                self.cash_position += monthly_savings 

            #performance tracking for later visualisation
            daily_stats = self.get_daily_stats(date)
            self.portfolio_history.append(daily_stats)
            
            #check for rebalance
            if date.day == 1 and date.month%6 == 1:# adjust to inputsettings
                self.rebalance(date)

            elif True:#TDOD: more options
                pass

            
    def get_daily_stats(self, date: datetime):
        stats = [self.cash_position]
        for asset in self.assets:
            asset_value = asset.total_amount*asset.get_price_from_date(date)
            stats.append(asset_value)
        return np.asarray(stats)
            

    def check_all_assets_valid_in_timeinterval(self, start_date, end_date):
        for asset in self.assets:
            if start_date not in asset.dates:
                raise ValueError(f'Start date "{start_date}" not in asset "{asset.key_name}"!')
            if end_date not in asset.dates:
                raise ValueError(f'End date "{start_date}" not in asset "{asset.key_name}"!')


    def rebalance(self, date:datetime):
        total_value = self.calculate_total_value(date)

        #TODO: buy and sell can be combined if enough accuracy in cash terms is acchieved (including fees, taxes)
        # and further preassignment takes place
        self.sell_over_positions(total_value, date)
        updated_total_value = self.calculate_total_value(date)
        self.buy_under_positions(updated_total_value, date)

    def calculate_total_value(self, date:datetime):
        total_value = self.cash_position
        for asset in self.assets:
            asset_value = asset.get_price_from_date(date) * asset.total_amount
            total_value += asset_value
        return total_value



    def sell_over_positions(self, total_portfolio_value, date:datetime):
        for asset in self.assets:
            if (rebalance_amount := asset.rebalance_amount(total_portfolio_value, date)) > 0:
                sell_order = asset.sell_amount(rebalance_amount, date)
                self.combined_order_history.append(sell_order)
                recieved_cash = sell_order.amount*sell_order.order_price-(sell_order.fees+sell_order.tax)
                self.cash_position += recieved_cash

            
    def buy_under_positions(self, total_portfolio_value, date:datetime):
        for asset in self.assets:
            if (rebalance_amount := asset.rebalance_amount(total_portfolio_value, date)) - 0:
                buy_order = asset.buy_amount(rebalance_amount, date)
                self.combined_order_history.append(buy_order)

                used_cash = buy_order.amount*buy_order.order_price-(buy_order.fees+buy_order.tax)
                self.cash_position -= used_cash

    # def handle_holding_cost(self):
    #     pass