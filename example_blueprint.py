from deposits import PureCash, DistributedCash, FixedShare, DynamicShare
from triggers import TimeUnit, DeviationType, TimeTrigger, DeviationTrigger
from investmentclasses import Share, Crypto, Commodity

 
portfolio_blueprint_0d = {
    'initial_cash': 5000, 
    'asset': [
        {'class': Share, 
         'key': 'msciworld', 
         'ratio': 7,
         }, 
        {'class': Share, 
         'key': 'msciem', 
         'ratio': 3}
    ], 
    'rebalancer': [
        {'class': DeviationTrigger, 
         'deviation_type': DeviationType.RELATIVE,
         'deviation_threshold': 5
         }, 
        {'class': TimeTrigger, 
         'time_unit': TimeUnit.MONTHS, 
         'time_interval': 6}
    ], 
    'deposit': [
        {'class': PureCash, 
         'deposit_value': 500, 
         'triggers':[
            {'class': TimeTrigger,
            'time_unit': TimeUnit.MONTHS, 
            'time_interval': 6}
         ]
        }
    ]
} 

portfolio_blueprint_1d = {
    'initial_cash': 5000, 
    'asset': [
        {'class': Share, 
         'key': 'msciworld', 
         'ratio': 7,
         }, 
        {'class': Share, 
         'key': 'msciem', 
         'ratio': 3}
    ], 
    'rebalancer': [
        {'class': DeviationTrigger, 
         'deviation_type': DeviationType.RELATIVE,
         'deviation_threshold': 5
         }, 
        {'class': TimeTrigger, 
         'time_unit': TimeUnit.MONTHS, 
         'time_interval': 6}
    ], 
    'deposit': [
        {'class': PureCash, 
         'deposit_value': 500, 
         'triggers':[
            {'class': TimeTrigger,
            'time_unit': TimeUnit.MONTHS, 
            'time_interval': [1,6,5,'lin','deposit_interval']}
         ]
        }
    ]
}

