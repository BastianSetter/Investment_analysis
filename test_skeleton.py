from deposits import PureCash, DistributedCash, FixedShare, DynamicShare
from triggers import 


portfolio_sceleton = {
    'initial_cash': 5000, 
    'asset': [
        {'class': 'share', 
         'key': 'msciworld', 
         'ratio': 7,
         }, 
        {'class': 'share', 
         'key': 'msciem', 
         'ratio': 3}
    ], 
    'rebalancer': [
        {'class': 'deviation', 
         'deviation_type': 'r',
         'deviation_threshold': 5
         }, 
        {'triggertype': 'time', 
         'timeunit': 'm', 
         'value': 6}
    ], 
    'deposit': [
        {'class': 'cash_fixed', 
        'amount': 500, 
        'timeunit': 'm', 
        'interval': 2}
    ]
}

depositer_map={
    'cash_fixed': PureCash,
    'cash_dyn': DistributedCash,
    'share_fixed': FixedShare,
    'share_dyn': DynamicShare
}
rebalancer = {

}