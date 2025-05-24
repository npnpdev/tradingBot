import os
import pandas as pd

FILENAME = 'variables.conf'
HISTORICAL_DAYS = 60
SHORT_WINDOW = 50
LONG_WINDOW = 200
SLEEP_TIME_BETWEEN_TRADES = 3  # in seconds
RSI_PERIOD = 14  # Okres dla obliczeń RSI

def load_config_from_file(filename):
    """
    Wczytuje zmienne z pliku konfiguracyjnego, ignorując linie komentarza zaczynające się od #.

    :param filename: Ścieżka do pliku konfiguracyjnego
    :return: Słownik zawierający zmienne konfiguracyjne
    """
    config = {
        "WALLET": 0,
        "SYMBOL": 'BTCUSDT',
        "INTERVAL": '1h',
        "STOP_LOSS_PERCENTAGE": 0.002,
        "TAKE_PROFIT_PERCENTAGE": 0.003,
        "PERCENTAGE_TO_INVEST": 0.3
    }

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                # Skip lines that are comments or empty
                if line.startswith('#') or not line:
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    if key == "WALLET":
                        config[key] = float(value)
                    elif key in ["STOP_LOSS_PERCENTAGE", "TAKE_PROFIT_PERCENTAGE", "PERCENTAGE_TO_INVEST"]:
                        config[key] = float(value)
                    else:
                        config[key] = value
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony. Używam domyślnych wartości.")
    except ValueError:
        print(f"Niepoprawny format danych w pliku {filename}. Używam domyślnych wartości.")
    except Exception as e:
        print(f"Wystąpił błąd podczas wczytywania konfiguracji: {e}")
    
    return config

def save_wallet_to_file(filename, wallet_value):
    """
    Zapisuje wartość portfela do pliku konfiguracyjnego.

    :param filename: Ścieżka do pliku konfiguracyjnego
    :param wallet_value: Wartość portfela do zapisania
    """
    config = load_config_from_file(filename)
    amount_to_trade = config["WALLET"] * config["PERCENTAGE_TO_INVEST"]
    config["WALLET"] = config["WALLET"] - amount_to_trade + wallet_value

    try:
        with open(filename, 'w') as file:
            for key, value in config.items():
                if isinstance(value, float):
                    file.write(f"{key} = {value:.6f}\n")
                else:
                    file.write(f"{key} = {value}\n")
        print(f"Wartość portfela została zapisana do pliku {filename}.")
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisywania portfela: {e}")

# Load configuration at the start
config = load_config_from_file(FILENAME)

# Initialize variables
WALLET = config["WALLET"]
SYMBOL = config["SYMBOL"]
INTERVAL = config["INTERVAL"]
STOP_LOSS_PERCENTAGE = config["STOP_LOSS_PERCENTAGE"]
TAKE_PROFIT_PERCENTAGE = config["TAKE_PROFIT_PERCENTAGE"]
PERCENTAGE_TO_INVEST = config["PERCENTAGE_TO_INVEST"]

def update_wallet(amount_to_invest):
    global WALLET
    WALLET = amount_to_invest
    save_wallet_to_file(FILENAME, amount_to_invest)
    print("Nowa wartość portfela: ", WALLET)

def get_wallet():
    global WALLET
    amount_to_invest = WALLET
    return amount_to_invest

def save_trade_result(result):
    """
    Zapisuje wynik trade do pliku konfiguracyjnego w formacie W/D/L.

    :param filename: Ścieżka do pliku konfiguracyjnego
    :param result: Krotka zawierająca wynik (W, D, L), np. (1, 0, 0) dla wygranej
    """
    # Wczytaj istniejącą konfigurację
    config = load_config_from_file(FILENAME)
    
    # Zaktualizuj wynik trade
    current_result = config.get("RESULT", "0/0/0")
    wins, draws, losses = map(int, current_result.split('/'))

    wins += result[0]
    draws += result[1]
    losses += result[2]

    config["RESULT"] = f"{wins}/{draws}/{losses}"

    try:
        # Zapisz zaktualizowaną konfigurację do pliku
        with open(FILENAME, 'w') as file:
            for key, value in config.items():
                if isinstance(value, float):
                    file.write(f"{key} = {value:.6f}\n")
                else:
                    file.write(f"{key} = {value}\n")
        print(f"Wynik trade został zapisany do pliku {FILENAME}.")
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisywania wyniku trade: {e}")

# Funkcja zapisująca dane po otwarciu lub zamknięciu pozycji
# Funkcja save_trade_log
def save_trade_log(trade_number, position_type, open_time, sma_short, sma_long, macd, macd_long, rsi, wallet):
    """
    Zapisuje wyniki handlu do pliku CSV.
    """
    # Sprawdź, czy plik istnieje
    file_exists = os.path.isfile("trade_log.csv")
    
    sma_signal = None
    macd_signal = None

    if sma_short['value'] > sma_long['value']:
        sma_signal = "buy"
    elif sma_short['value'] < sma_long['value']:
        sma_signal = "sell"

    if macd['value'] > macd_long['value']:
        macd_signal = "buy"
    elif macd['value'] < macd_long['value']:
        macd_signal = "sell"

    # Tworzenie DataFrame do zapisania
    trade_data = {
        "trade_number": trade_number,
        "position_type": position_type,
        "open_time": open_time,
        "duration": 0,  # Zamień na format string
        "sma_short_value": sma_short['value'],
        "sma_long_value": sma_long['value'],  # Dodaj SMA_long
        "sma_signal": sma_signal,  
        "macd_value": macd['value'],
        "macd_long_value": macd_long['value'],  # Dodaj MACD_long
        "macd_signal": macd_signal, 
        "rsi_value": rsi['value'],
        "rsi_signal": rsi['signal'],
        "wallet": wallet
    }
    
    trade_df = pd.DataFrame([trade_data])
    
    # Zapisz do CSV
    if file_exists:
        trade_df.to_csv("trade_log.csv", mode='a', header=False, index=False)
    else:
        trade_df.to_csv("trade_log.csv", mode='w', header=True, index=False)

def get_trade_number(position_type):
    """
    Oblicza numer następnej pozycji na podstawie wyniku trade zapisanego w formacie W/D/L w pliku konfiguracyjnym.

    :param filename: Ścieżka do pliku konfiguracyjnego
    :return: Numer następnej pozycji
    """
    # Wczytaj istniejącą konfigurację
    config = load_config_from_file(FILENAME)
    
    # Pobierz wynik trade w formacie W/D/L
    current_result = config.get("RESULT", "0/0/0")
    wins, draws, losses = map(int, current_result.split('/'))

    # Oblicz liczbę otwartych do tej pory pozycji
    total_trades = wins + draws + losses

    if(position_type == "open"):
        return total_trades + 1
    else:
        return total_trades