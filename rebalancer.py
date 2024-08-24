import numpy as np
from datetime import date
from abc import ABC, abstractmethod
from triggers import Trigger

def update_converged(old_changes, updated_changes)->bool:
    maximum_allowed_change = 1
    if any(np.abs(new - old)>maximum_allowed_change for new, old in zip(updated_changes, old_changes)):
        return False
    else: 
        return True


class Rebalancer():
    def __init__(self) -> None:
        self.triggers = []

    def add_trigger(self, trigger:Trigger):
        self.triggers.append(trigger)

    def rebalance(self, date:date, portfolio):
        #check for rebalance
        rebalance_today = False
        for trigger in self.triggers:
            trigger.check_trigger(date, portfolio)
        if not rebalance_today: return 

        self.execute_rebalance(date, portfolio)

    def execute_rebalance(self, date, portfolio):
        #TODO: include a minimum transaction value, to reduce unnecessary fees
        
        for asset in portfolio.assets:
            asset.update_cost_function_table()
        
        changes = [0]*len(portfolio.assets)
        while True:
            #BEWARY: wann sind costs in changes und total value drin: Oscilieren?
            total_value = portfolio.calculate_total_value(date, changes = changes)
            new_changes = [total_value*asset.target_ratio - asset.current_value(date) for asset in portfolio.assets]
            if update_converged(changes, new_changes): break
            changes = new_changes

        for asset, change in zip(portfolio.assets, new_changes):
            if change>0:
                buy_order = asset.buy_per_value(change, date)
                portfolio.combined_order_history.append(buy_order)
                portfolio.cash_position -= change
            elif change<0:
                sell_order = asset.sell_per_value(change, date)
                portfolio.combined_order_history.append(sell_order)
                portfolio.cash_position += (change-sell_order.fees-sell_order.tax)


