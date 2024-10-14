from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from numbers import Number
from typing import Tuple, List
from propagation import Portfolio
from copy import deepcopy
from icecream import ic
from visualisation import plot_1D_metrics
from random import choices
#typehinting
import propagation
import investmentclasses


def identifiy_variations(blueprint, found_patterns = None, counter = 0) -> Tuple['propagation.Portfolio',List, int]:
    if found_patterns is None:
        found_patterns = []
    
    if isinstance(blueprint, dict):
        for key, value in blueprint.items():
            blueprint[key], found_patterns, counter = identifiy_variations(value, found_patterns, counter)
    elif isinstance(blueprint, list):
        if pattern_matches(blueprint):
            found_patterns.append(blueprint)  
            replacement_value = f"x{counter}"  
            return replacement_value, found_patterns, counter + 1  
        else:
            new_list = []
            for item in blueprint:
                new_item, found_patterns, counter = identifiy_variations(item, found_patterns, counter)
                new_list.append(new_item)
            return new_list, found_patterns, counter
    return blueprint, found_patterns, counter

def pattern_matches(item:list) -> bool:
    return len(item) == 5 and isinstance(item[0], Number) and isinstance(item[1], Number) \
        and isinstance(item[2], Number) and isinstance(item[3], str) and isinstance(item[4], str)



def analyse_single_config(portfolio:'propagation.Portfolio'):
    ...

def analyse_1D_variation(base_portfolio:'propagation.Portfolio', variation):
    variation_range = construct_variation_range(variation)
    combined_metrics = []
    for var in variation_range:
        ic(var)
        local_portfolio_struct = insert_specific(deepcopy(base_portfolio), 'x0', var)
        local_portfolio = Portfolio.from_dict(local_portfolio_struct)
        metric_values = analyse_portfolio(local_portfolio)
        combined_metrics.append(metric_values)

    combined_metrics = np.array(combined_metrics).T

    plot_1D_metrics(variation, variation_range, combined_metrics)

def analyse_2D_variation(base_portfolio, variations):
    ...



def construct_variation_range(variation):
    if variation[3] == 'linear':
        return np.linspace(*variation[0:3])
    elif variation[3] == 'log':
        return np.logspace(*variation[0:3])
    
def insert_specific(d:dict, search_value:str, variation_value)->'propagation.Portfolio':
    if isinstance(d, dict):
        for key, value in d.items():
            d[key] = insert_specific(value, search_value, variation_value)
    elif isinstance(d, list):
        return [insert_specific(item, search_value, variation_value) for item in d]
    elif d == search_value:
        return variation_value
    return d

def analyse_portfolio(portfolio:'propagation.Portfolio', repetitions = 20):   
    maximum_timeFrame = determine_maximum_testing_timeframe(portfolio)

    metric_values = []
    for timeframe in generate_random_timeframes(repetitions, maximum_timeFrame):
        simulation_trace = portfolio.simulate_timeinterval(*timeframe)
        metric_values.append(simulation_trace.get_metrics())
    # ic(metric_values)
    return np.mean(metric_values, axis=0)

def determine_maximum_testing_timeframe(portfolio:'propagation.Portfolio'):
    start = portfolio.get_first_common_date()
    end = portfolio.get_last_common_date()
    return (start, end)

def generate_random_timeframes(repetitions, maximum_timeframe, 
                               option = {'type': 'random', 'sample_percent': 0.1}
                               #{'type':'consecutive', 'spacing': 2}
                               ):
    if repetitions == 1: 
        yield maximum_timeframe
        return
    
    match option["type"]:
        case 'consecutive':
            max_offset = repetitions * option["spacing"]
            offsets = range(0, max_offset, option["spacing"])
        
        case 'random':
            max_timeframe_days = (maximum_timeframe[1]-maximum_timeframe[0]).days
            max_offset = max([int(max_timeframe_days * option["sample_percent"]), repetitions])
            offsets = choices(range(max_offset), k = repetitions)

        case _:
            raise KeyError(f'{option["type"]} is not a valid generation option.')
        
    for offset in offsets:
        start = maximum_timeframe[0]+timedelta(days=offset)
        end = maximum_timeframe[1]-timedelta(days=max_offset-offset)
        yield (start, end)








    




            


