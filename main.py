import time
from config import SYMBOL, FILENAME, load_config_from_file, WALLET, PERCENTAGE_TO_INVEST
from data_fetcher import prepare_historical_data
from trading import trade_loop

def main():
    """
    Główna pętla aplikacji, która symuluje ruch ceny BTC/USDT na podstawie danych historycznych.
    """
    load_config_from_file(FILENAME)

    amount_to_invest = WALLET * PERCENTAGE_TO_INVEST

    # Przygotowanie danych historycznych
    historical_data = prepare_historical_data()
    if historical_data is None or len(historical_data) == 0:
        print("Nie udało się pobrać danych historycznych.")
        return

    print(f"Pobrano {len(historical_data)} historycznych cen dla {SYMBOL}.")

    # Poczekaj minutę przed rozpoczęciem handlu
    print("Poczekaj minutę, zbieranie danych...")
    time.sleep(3)

    # Rozpoczęcie pętli handlowej
    trade_loop(historical_data, amount_to_invest)

if __name__ == "__main__":
    main()