import talib
from config import SHORT_WINDOW, LONG_WINDOW

def calculate_indicators(data):
    """
    Funkcja oblicza wskaźniki techniczne.
    """
    # Używamy TA-Lib do obliczenia prostych średnich kroczących
    data['SMA_short'] = talib.SMA(data['close'], timeperiod=SHORT_WINDOW)
    data['SMA_long'] = talib.SMA(data['close'], timeperiod=LONG_WINDOW)
    
    # Obliczamy MACD i jego sygnał
    macd, macd_signal, macd_hist = talib.MACD(data['close'])
    data['MACD'] = macd
    data['MACD_signal'] = macd_signal
    
    # Debugging: Wyświetl wartości wskaźników z aktualną ceną i datą
    latest_row = data.iloc[-1]
    print(f"Debug: Data: {latest_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Debug: Cena: {latest_row['close']:.2f}")
    print(f"Debug: SMA_short: {latest_row['SMA_short']:.2f}, SMA_long: {latest_row['SMA_long']:.2f}")
    print(f"Debug: MACD: {latest_row['MACD']:.2f}, MACD_signal: {latest_row['MACD_signal']:.2f}")