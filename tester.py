from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
#typehinting
import propagation
import investmentclasses



class Tester():
    def __init__(self, portfolio:'propagation.Portfolio') -> None:
        self.portfolio = portfolio

    def determine_maximum_testing_timeframe(self):
        start = self.portfolio.get_first_common_date()
        end = self.portfolio.get_last_common_date()
        return (start, end)
    
    def test_portfolio_multiple_times(self, timeframe:tuple[date, date] | None = None, repetitions = 7):
        if timeframe is None:
            timeframe = self.determine_maximum_testing_timeframe()

        simulation_traces = []
        #TODO: make into random sampling in start range based of trigger repetition
        for offset in range(repetitions):
            start = timeframe[0]+timedelta(days=offset)
            end = timeframe[1]
            simulation_trace = self.portfolio.simulate_timeinterval(start, end)
            simulation_traces.append(simulation_trace)

        return simulation_traces

    def calculate_internal_rate_of_return(self, sim_trace: 'propagation.Simulation_trace'):
        end_date:date = sim_trace.stats[-1][0]
        final_portfolio_value = np.sum(sim_trace.stats[-1][1:])

        best_irr_approx = 0
        best_difference = np.inf
        for irr in np.linspace(0,10,10000):
            result = 0
            for deposit in sim_trace.deposits:
                invest_duration = (end_date-deposit.date).days/365.2425
                result += deposit.value*(1+irr)**invest_duration

            approx_diff = np.abs(result-final_portfolio_value)
            if approx_diff < best_difference:
                best_difference = approx_diff
                best_irr_approx = irr
            else: break

        return best_irr_approx

    # def calculate_lost_costs(self, sim_trace: 'propagation.Simulation_trace'):
    #     ...
    #     # run an additional simulation with no taxes and or fees

    def calculate_lost_costs(self, sim_trace: 'propagation.Simulation_trace'):
        fees = 0
        taxes = 0
        for order in sim_trace.orders:
            fees += order.fees
            taxes += order.tax
        return (fees, taxes)
    
    #TODO: variable variation based on dict generation
    





            


