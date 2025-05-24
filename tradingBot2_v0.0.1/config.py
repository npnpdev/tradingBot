FILENAME = 'variables.conf'
SHORT_WINDOW = 50
LONG_WINDOW = 200
SLEEP_TIME_BETWEEN_TRADES = 3  # in seconds

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
