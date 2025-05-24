import time
from strategy import moving_average_crossover_strategy
from simulator import simulate_trading
from config import LONG_WINDOW, SLEEP_TIME_BETWEEN_TRADES, get_wallet, update_wallet

def trade_loop(historical_data, amount_to_invest):
    """
    Główna pętla handlowa, która analizuje dane i podejmuje decyzje na podstawie strategii.
    """
    position = None
    entry_price = None

    try:
        # Symulacja, która wykorzystuje dane historyczne
        index = LONG_WINDOW  # Zaczynamy od okresu SMA
        while index < len(historical_data):
            # Przekazujemy podzbiór danych do strategii
            subset_data = historical_data.iloc[:index+1]

            # Wywołujemy strategię i aktualizujemy zmienną position oraz entry_price
            position, entry_price = moving_average_crossover_strategy(subset_data, amount_to_invest)

            # Jeśli pozycja jest otwarta, symulujemy handel
            if position:
                simulate_trading(historical_data, index, position, entry_price, amount_to_invest)
                amount_to_invest = get_wallet()

            # Czekaj 5 sekund przed kolejnym krokiem
            time.sleep(SLEEP_TIME_BETWEEN_TRADES)
            index += 1  # Przechodzimy do następnego indeksu

    except KeyboardInterrupt:
        update_wallet(amount_to_invest)
        print("Symulacja przerwana.")
