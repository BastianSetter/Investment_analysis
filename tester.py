from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from numbers import Number
from typing import Tuple, List
#typehinting
import propagation
import investmentclasses



class Tester():
    def __init__(self, portfolio:'propagation.Portfolio') -> None:
        self.base_portfolio, self.variations, self.counter = self.identifiy_variations(portfolio)
        if self.counter == 0:
            self.make_run_plots()
        elif self.counter == 1:
            self.make_1D_plots(self.variations[0])
        elif self.counter == 2:
            self.make_2D_plots(self.variations)
        else:
            print('Tooo many variations.')

    def identifiy_variations(self, blueprint, found_patterns=None, counter=0)->Tuple['propagation.Portfolio',List, int]:
        if found_patterns is None:
            found_patterns = []
        
        if isinstance(blueprint, dict):
            for key, value in blueprint.items():
                blueprint[key], found_patterns, counter = self.identifiy_variations(value, found_patterns, counter)
        elif isinstance(blueprint, list):
            if self.pattern_matches(blueprint):
                found_patterns.append(blueprint)  # Store the found pattern
                replacement_value = f"x{counter}"  # Create 'x0', 'x1', ...
                return replacement_value, found_patterns, counter + 1  # Increment counter
            else:
                new_list = []
                for item in blueprint:
                    new_item, found_patterns, counter = self.identifiy_variations(item, found_patterns, counter)
                    new_list.append(new_item)
                return new_list, found_patterns, counter
        return blueprint, found_patterns, counter

    def pattern_matches(self, item:list)->bool:
        return len(item) == 5 and isinstance(item[0], Number) and isinstance(item[1], Number) \
            and isinstance(item[2], Number) and isinstance(item[3], str) and isinstance(item[4], str)

    def construct_variation_range(self, variation):
        if variation[3] == 'lin':
            return np.linspace(*variation[0:3])
        elif variation[3] == 'log':
            return np.logspace(*variation[0:3])
        
    def insert_specific(self, d:dict, search_value, variation_value)->'propagation.Portfolio':
        if isinstance(d, dict):
            for key, value in d.items():
                d[key] = self.insert_specific(value)
        elif isinstance(d, list):
            return [self.insert_specific(item) for item in d]
        elif d == search_value:  # If we find 'x', replace it with 1
            return variation_value
        return d
    
    def determine_maximum_testing_timeframe(self):
        start = self.portfolio.get_first_common_date()
        end = self.portfolio.get_last_common_date()
        return (start, end)
    
    def test_portfolio_multiple_times(self, timeframe:tuple[date, date] | None = None, repetitions = 7):
        if timeframe is None:
            timeframe = self.determine_maximum_testing_timeframe()

        simulation_traces = []
        #TODO: make into random sampling in start range based of trigger repetition (comected with central referncedate)
        for offset in range(repetitions):
            start = timeframe[0]+timedelta(days=offset)
            end = timeframe[1]
            simulation_trace = self.base_portfolio.simulate_timeinterval(start, end)
            simulation_traces.append(simulation_trace)

        return simulation_traces

    def make_run_plots(self):
        ...
    
    def make_1D_plots(self, variation):
        variation_range = self.construct_variation_range(variation)
        metric_values = []
        for step in variation_range:
            local_portfolio = self.insert_specific(self.base_portfolio, 'x0', step)
            timeframe = self.determine_maximum_testing_timeframe()
            metrics = local_portfolio.simulate_timeinterval(*timeframe)
            metric_values.append(metrics)
        metric_values = np.array(metric_values).T

        fig, axes = plt.subplots(1,2, figsize = (8,3))
        for counter, ax in enumerate(axes):
            ax.plot(variation_range, metric_values[counter])
            ax.set_xscale(variation[3])
            ax.set_xlabel(variation[4])
        ax[0].set_ylabel('IRR')
        ax[1].set_ylable('Costs')
        fig.show()

    def make_2D_plots(self, variations):
        ...



    




            


