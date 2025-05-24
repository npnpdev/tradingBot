import requests
import pandas as pd
from datetime import datetime, timedelta
from config import SYMBOL, INTERVAL, HISTORICAL_DAYS
from indicators import calculate_indicators

def get_historical_data(start_time, end_time):
    """
    Funkcja pobierająca historyczne dane cenowe z Binance.
    Zwraca DataFrame z danymi.
    """
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'startTime': int(start_time.timestamp() * 1000),
        'endTime': int(end_time.timestamp() * 1000),
        'limit': 1000
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        # Przechowujemy dane w DataFrame
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = df['close'].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Błąd podczas pobierania danych historycznych: {e}")
        return None

def prepare_historical_data():
    """
    Przygotowanie danych historycznych wraz z obliczeniami wskaźników.
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=HISTORICAL_DAYS)

    # Pobieranie danych historycznych
    historical_data = get_historical_data(start_time, end_time)
    
    if historical_data is not None and len(historical_data) > 0:
        # Obliczamy wskaźniki techniczne
        calculate_indicators(historical_data)

    return historical_data
