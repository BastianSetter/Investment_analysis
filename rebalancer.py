import numpy as np
from datetime import date
from abc import ABC, abstractmethod
from triggers import Trigger

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
        #TODO: buy and sell can be combined if enough accuracy in cash terms is acchieved (including fees, taxes)
        # and further preassignment takes place
        self.sell_over_positions(portfolio, date)
        self.buy_under_positions(portfolio, date)

    def sell_over_positions(self, portfolio, date:date):
        total_portfolio_value = portfolio.calculate_total_value(date)
        for asset in portfolio.assets:
            if (rebalance_amount := asset.rebalance_amount(total_portfolio_value, date)) > 0:
                sell_order = asset.sell_amount(rebalance_amount, date)
                portfolio.combined_order_history.append(sell_order)
                recieved_cash = sell_order.amount*sell_order.order_price-(sell_order.fees+sell_order.tax)
                portfolio.cash_position += recieved_cash

            
    def buy_under_positions(self, portfolio, date:date):
        total_portfolio_value = portfolio.calculate_total_value(date)
        for asset in portfolio.assets:
            if (rebalance_amount := asset.rebalance_amount(total_portfolio_value, date)) - 0:
                buy_order = asset.buy_per_piece(-rebalance_amount, date)
                portfolio.combined_order_history.append(buy_order)
                used_cash = buy_order.amount*buy_order.order_price-(buy_order.fees+buy_order.tax)
                portfolio.cash_position -= used_cash


