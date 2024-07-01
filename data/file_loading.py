from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from scipy.interpolate import interp1d

def load_data(key) -> np.ndarray:
    match key:
        case 'msciworld':
            data = load_msci_world()
        case 'msciem':
            data = load_msci_em()
        case _:     
            raise 'Wrong key!'
    
    data = extrapolate_missing_dates(data)
    return data
        
def extrapolate_missing_dates(data):
    dates, prices = data

    full_dates = [dates[0] + timedelta(days=i) for i in range((dates[-1] - dates[0]).days + 1)]
    full_date_nums = mdates.date2num(full_dates)
    
    date_nums = mdates.date2num(dates)
    interp_func = interp1d(date_nums, prices, kind='linear', fill_value="extrapolate")
    interpolated_prices = interp_func(full_date_nums)

    return (np.array(full_dates), interpolated_prices)


def load_msci_world():
    df = pd.read_excel(r'C:\Users\basti\PythonScripts\Investment_analysis\data\MSCI_WORLD.xlsx', sheet_name='IE00BJ0KDQ92', skiprows=13)
    dates = df['Date'].values
    datetime_dates = np.array([datetime.strptime(date, "%d.%m.%Y") for date in dates])

    prices = df['NAV'].values
    return (datetime_dates, prices)

def load_msci_em():
    df = pd.read_excel(r'C:\Users\basti\PythonScripts\Investment_analysis\data\MSCI_WORLD.xlsx', sheet_name='IE00BJ0KDQ92', skiprows=13)
    dates = df['Date'].values
    datetime_dates = np.array([datetime.strptime(date, "%d.%m.%Y") for date in dates])

    prices = df['NAV'].values
    return (datetime_dates, prices)

