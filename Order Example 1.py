from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *
import requests
from time import sleep

g_api_key = "bg5t6ygr6y-52449ec9-dcb2794e-160fa"
g_secret_key = "c3518e09-d6d8b84b-3c44670d-4679b"

trade_client = TradeClient(api_key=g_api_key, secret_key=g_secret_key)

while True:
    try:
        btc = requests.get('https://api.huobi.pro/market/detail/merged?symbol=btcusdt').json()
        print(btc['tick']['ask'][0])
    except Exception as e:
        print(f'Error obtaining BTC data: {e}')
        
    if btc['tick']['ask'][0] < 31000.00:
        print('Order requirment not reached.')
        continue
        
    else:
        try:
            order = trade_client.create_order(symbol='ethusdc', account_id=30316484, 
                                              order_type=OrderType.BUY_LIMIT, source=OrderSource.API, 
                                              amount=0.005, price=2000.00)
        except Exception as e:
            print(f'Order failed to execute: {e}')
    
        sleep(2)

        try:
            check_order = trade_client.get_order(order)
            print(check_order)
        except Exception as e:
            print(f'Failed to check order details. {e}')
        
        check = check_order.get_state()

        if check != 'canceled':
            print('Order executed successfully!')
            break
        else:
            print('Order was canceled!')
            break