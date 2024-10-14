import numpy as np
from icecream import ic
#typehinting
from datetime import date as dt
import triggers
import propagation

def update_converged(old_changes, updated_changes)->bool:
    maximum_allowed_change = 0.1
    for new, old in zip(updated_changes, old_changes):
        if np.abs(new - old)>maximum_allowed_change:
            return False
    return True


class Rebalancer():
    def __init__(self) -> None:
        self.triggers = []

    def add_trigger(self, trigger:'triggers.Trigger'):
        self.triggers.append(trigger)

    def rebalance(self, date:dt, portfolio:'propagation.Portfolio'):
        answers = [trigger.check_trigger(date, portfolio) for trigger in self.triggers]
        if any(answers): 
            self.execute_rebalance(date, portfolio)

    def execute_rebalance(self, date:dt, portfolio:'propagation.Portfolio'):
        #TODO: include a minimum transaction value, to reduce unnecessary fees
        #TODO: option to only buy with best rebalance
        
        for asset in portfolio.assets:
            asset.update_cost_function_table(date)
        
        changes = [0]*len(portfolio.assets)

        while True:
            total_value = portfolio.calculate_total_value(date, changes = changes)
            new_changes = []
            for asset in portfolio.assets:
                change = total_value * asset.target_ratio - asset.get_current_value(date)
                new_changes.append(change)

            if update_converged(changes, new_changes): break
            changes = new_changes

        for asset, change in zip(portfolio.assets, new_changes):
            if change>0:
                buy_order = asset.buy_per_value(change, date)
                portfolio.combined_order_history.append(buy_order)
                portfolio.cash_position -= (change + buy_order.fees + buy_order.tax)
            elif change<0:
                sell_order = asset.sell_per_value(change, date)
                portfolio.combined_order_history.append(sell_order)
                portfolio.cash_position -= (change + sell_order.fees + sell_order.tax)
    