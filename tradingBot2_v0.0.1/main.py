import time
from datetime import datetime, timedelta
from config import SYMBOL, LONG_WINDOW, SLEEP_TIME_BETWEEN_TRADES, WALLET, PERCENTAGE_TO_INVEST, FILENAME, get_wallet, save_wallet_to_file, load_config_from_file
from data_fetcher import get_historical_data
from indicators import calculate_indicators
from strategy import moving_average_crossover_strategy
from simulator import simulate_trading

def main():
    """
    Główna pętla aplikacji, która symuluje ruch ceny BTC/USDT na podstawie danych historycznych.
    """

    load_config_from_file(FILENAME)

    position = None  # Inicjalizuj lokalną zmienną position
    entry_price = None  # Inicjalizuj lokalną zmienną entry_price
    amount_to_invest = WALLET * PERCENTAGE_TO_INVEST

    # Ustawienia historycznych danych
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)  # Pół roku temu

    # Pobranie danych historycznych
    historical_data = get_historical_data(start_time, end_time)
    if historical_data is None or len(historical_data) == 0:
        print("Nie udało się pobrać danych historycznych.")
        return

    # Obliczamy wskaźniki techniczne
    calculate_indicators(historical_data)

    print(f"Pobrano {len(historical_data)} historycznych cen dla {SYMBOL}.")

    # Poczekaj minutę przed rozpoczęciem handlu
    print("Poczekaj minutę, zbieranie danych...")
    time.sleep(3)

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
        save_wallet_to_file(FILENAME, amount_to_invest)
        print("Symulacja przerwana.")

if __name__ == "__main__":
    main()
