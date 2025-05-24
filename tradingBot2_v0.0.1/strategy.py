import pandas as pd

def decision_maker(data):
    """
    Funkcja decyzyjna oparta na kombinacji sygnałów wskaźników.
    """
    latest_row = data.iloc[-1]
    
    buy_signals = 0
    sell_signals = 0

    # Sprawdź wskaźniki
    if pd.notna(latest_row['SMA_short']) and pd.notna(latest_row['SMA_long']):
        if latest_row['SMA_short'] > latest_row['SMA_long']:
            buy_signals += 1
        elif latest_row['SMA_short'] < latest_row['SMA_long']:
            sell_signals += 1

    if pd.notna(latest_row['MACD']) and pd.notna(latest_row['MACD_signal']):
        if latest_row['MACD'] > latest_row['MACD_signal']:
            buy_signals += 1
        elif latest_row['MACD'] < latest_row['MACD_signal']:
            sell_signals += 1

    # Debugging: Wyświetl wartości wskaźników
    print(f"Debug: Data: {latest_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Debug: Cena: {latest_row['close']:.2f}")
    
    print(f"Debug: SMA_short: {latest_row['SMA_short']:.2f}, SMA_long: {latest_row['SMA_long']:.2f}")
    if pd.notna(latest_row['SMA_short']) and pd.notna(latest_row['SMA_long']):
        if latest_row['SMA_short'] > latest_row['SMA_long']:
            print("Debug: SMA sygnalizuje KUPNO (SMA_short > SMA_long)")
        elif latest_row['SMA_short'] < latest_row['SMA_long']:
            print("Debug: SMA sygnalizuje SPRZEDAŻ (SMA_short < SMA_long)")

    print(f"Debug: MACD: {latest_row['MACD']:.2f}, MACD_signal: {latest_row['MACD_signal']:.2f}")
    if pd.notna(latest_row['MACD']) and pd.notna(latest_row['MACD_signal']):
        if latest_row['MACD'] > latest_row['MACD_signal']:
            print("Debug: MACD sygnalizuje KUPNO (MACD > MACD_signal)")
        elif latest_row['MACD'] < latest_row['MACD_signal']:
            print("Debug: MACD sygnalizuje SPRZEDAŻ (MACD < MACD_signal)")

    # Podejmowanie decyzji
    if buy_signals > sell_signals:
        return 'buy'
    elif sell_signals > buy_signals:
        return 'sell'
    else:
        return 'hold'
    
def moving_average_crossover_strategy(data, amount_to_invest):
    """
    Strategia wykorzystująca decyzję podjętą przez funkcję decision_maker.
    """

    position = None  # Inicjalizuj lokalną zmienną position
    entry_price = None  # Inicjalizuj lokalną zmienną entry_price
    
    # Uzyskaj decyzję z funkcji decision_maker
    decision = decision_maker(data)

    latest_row = data.iloc[-1]
    
    # Podejmij decyzję
    if decision == 'buy' and position is None:
        # Otwieramy pozycję LONG
        position = {'type': 'long', 'price': latest_row['close'], 'amount': amount_to_invest / latest_row['close']}
        entry_price = latest_row['close']
        print(f"Kupno (LONG)! Cena: {latest_row['close']:.2f} Data: {latest_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    elif decision == 'sell' and position is None:
        # Otwieramy pozycję SHORT
        position = {'type': 'short', 'price': latest_row['close'], 'amount': amount_to_invest / latest_row['close']}
        entry_price = latest_row['close']
        print(f"Sprzedaż (SHORT)! Cena: {latest_row['close']:.2f} Data: {latest_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

    return position, entry_price