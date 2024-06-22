from datetime import datetime
import numpy as np
import pandas as pd
DATE_FORMAT = "%m.%d.%Y"

def load_data(key) -> np.ndarray:

    match key:
        case 'msciworld':
            data = load_msciworld()
        case _:     
            raise 'Wrong key!'
    
    #TODO: fill in  weakends etc or solve at computation

    return data
        

def load_msciworld():
    df = pd.read_excel(r'C:\Users\basti\PythonScripts\Investment_analysis\data\MSCIWORLD.xlsx', sheet_name='IE00BJ0KDQ92', skiprows=13)
    dates = df['Date'].values
    prices = df['NAV'].values
    return (dates, prices)
