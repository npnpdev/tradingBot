import time
from config import STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE, SLEEP_TIME_BETWEEN_TRADES, update_wallet

def simulate_trading(data, start_index, position, entry_price, amount_to_invest):
    """
    Symulacja handlu po otwarciu pozycji z mechanizmami stop loss i take profit.
    """
    current_index = start_index
    starting_amount = amount_to_invest
    
    while position:
        # Sprawdź, czy mamy wystarczająco danych
        if current_index >= len(data):
            print("Brak nowych danych do analizy.")
            return
        
        # Aktualizuj dane do najnowszej ceny
        latest_row = data.iloc[current_index]
        current_price = latest_row['close']
        current_date = latest_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Obliczanie poziomów stop loss i take profit
        if position['type'] == 'long':
            stop_loss_price = entry_price * (1 - STOP_LOSS_PERCENTAGE)
            take_profit_price = entry_price * (1 + TAKE_PROFIT_PERCENTAGE)
        elif position['type'] == 'short':
            stop_loss_price = entry_price * (1 + STOP_LOSS_PERCENTAGE)
            take_profit_price = entry_price * (1 - TAKE_PROFIT_PERCENTAGE)

        # Sprawdź warunki stop loss i take profit
        if position['type'] == 'long':
            if current_price <= stop_loss_price:
                print(f"Stop Loss aktywowany! Cena: {current_price:.2f} Data: {current_date}")
                # Oblicz zysk/stratę na podstawie długiej pozycji
                profit_or_loss = (current_price - entry_price) * position['amount']
                amount_to_invest += profit_or_loss  # Dodaj zysk/stratę do portfela
                position = None
                entry_price = None
                update_wallet(amount_to_invest)
                return
            
            if current_price >= take_profit_price:
                print(f"Take Profit osiągnięty! Cena: {current_price:.2f} Data: {current_date}")
                # Oblicz zysk/stratę na podstawie długiej pozycji
                profit_or_loss = (current_price - entry_price) * position['amount']
                amount_to_invest += profit_or_loss  # Dodaj zysk/stratę do portfela
                position = None
                entry_price = None
                update_wallet(amount_to_invest)
                return

        elif position['type'] == 'short':
            if current_price >= stop_loss_price:
                print(f"Stop Loss aktywowany! Cena: {current_price:.2f} Data: {current_date}")
                # Oblicz zysk/stratę na podstawie krótkiej pozycji
                profit_or_loss = (entry_price - current_price) * position['amount']
                amount_to_invest += profit_or_loss  # Dodaj zysk/stratę do portfela
                position = None
                entry_price = None
                update_wallet(amount_to_invest)
                return
    
            if current_price <= take_profit_price:
                print(f"Take Profit osiągnięty! Cena: {current_price:.2f} Data: {current_date}")
                # Oblicz zysk/stratę na podstawie krótkiej pozycji
                profit_or_loss = (entry_price - current_price) * position['amount']
                amount_to_invest += profit_or_loss  # Dodaj zysk/stratę do portfela
                position = None
                entry_price = None
                update_wallet(amount_to_invest)
                return

        # Wypisz aktualną wartość portfela i procentową zmianę
        if position['type'] == 'long':
            percentage_change = ((current_price - entry_price) / entry_price) * 100
        elif position['type'] == 'short':
            percentage_change = ((entry_price - current_price) / entry_price) * 100

        # Można zaktualizować wartość portfela, jeśli jest potrzebna
        amount_to_invest = starting_amount * (1 + (percentage_change / 100))

        print(f"Aktualna cena BTC/USDT: {current_price:.2f} Data: {current_date}")
        print(f"Wartość portfela: {amount_to_invest:.2f} USDT")
        print(f"Procentowa zmiana: {percentage_change:.2f}%")

        # Odczekiwanie na pobranie nowych danych
        time.sleep(SLEEP_TIME_BETWEEN_TRADES)
        
        # Przechodzimy do kolejnej ceny
        current_index += 1
