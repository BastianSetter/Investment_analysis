from deposits import PureCash, DistributedCash, FixedShare, DynamicShare
from triggers import TimeUnit, DeviationType, TimeTrigger, DeviationTrigger
from investmentclasses import Share, Crypto, Commodity


portfolio_blueprint = {
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
        {'triggertype': TimeTrigger, 
         'timeunit': TimeUnit.MONTHS, 
         'value': 6}
    ], 
    'deposit': [
        {'class': PureCash, 
        'amount': 500, 
        'timeunit': TimeUnit.MONTHS, 
        'interval': 2}
    ]
}

