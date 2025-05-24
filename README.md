# Trading Bot Simulator

[English](#english-version) | [Polski](#wersja-polska)

---

## English Version

**Project**: Trading Bot Simulator — real-time and historical data-driven cryptocurrency trading simulation.

**Description**: Connects to Binance for historical and real-time market data on a configurable trading pair, computes SMA, MACD, RSI indicators, applies a combined-signal strategy, executes simulated trades with stop-loss and take-profit, logs results to CSV, and updates wallet balance in config.

**Key Features**:

* **Data Fetching**: retrieves OHLC data via Binance API for a configurable trading pair, interval, and lookback period
* **Indicator Calculation**: computes SMA (short/long), MACD & signal line, RSI using TA-Lib
* **Decision Logic**: combines SMA, MACD, RSI signals to decide buy, sell or hold
* **Trade Simulation**: executes long/short positions, enforces stop-loss and take-profit rules
* **Logging & Persistence**: writes trade logs to CSV, updates wallet and W/D/L record in config file
* **Configurable Parameters**: adjustable wallet size, investment percentage, stop-loss/take-profit levels

**Tech Stack**:

* Python 3.x
* requests, pandas, TA-Lib
* Custom config parser

**Skills & Competencies**:

* Technical: API integration, data analysis, algorithmic trading strategies, backtesting frameworks
* Soft: problem-solving, attention to detail, adaptability, documentation

**Project Structure**:

```
📁 tradingBot2_v0.0.2
📁 tradingBot2_v0.0.1
├── main.py
├── config.py
├── data_fetcher.py
├── indicators.py
├── strategy.py
├── simulator.py
├── trading.py
├── variables.conf
├── trade_log.csv
```

## Wersja polska

**Projekt**: Trading Bot Simulator — symulacja handlu kryptowalutami w czasie rzeczywistym i na danych historycznych.

**Opis**: Łączy się z Binance w celu pobierania danych historycznych i w czasie rzeczywistym dla wybranej pary, oblicza wskaźniki SMA, MACD, RSI, stosuje strategię sygnałów, symuluje transakcje z mechanizmami stop-loss/take-profit, zapisuje logi do CSV i aktualizuje portfel.

**Kluczowe funkcje**:

* **Pobieranie danych**: API Binance, konfigurowalna para walutowa, interwał i okres danych historycznych
* **Obliczanie wskaźników**: SMA (krótka/długa), MACD i linia sygnału, RSI (TA-Lib)
* **Logika decyzji**: sygnały SMA, MACD i RSI razem decydują o kupnie, sprzedaży lub oczekiwaniu
* **Symulacja handlu**: pozycje long/short z regułami stop-loss i take-profit
* **Logi i trwałość**: zapisywanie transakcji do CSV, aktualizacja salda i wyniku W/D/L w pliku konfiguracyjnym
* **Parametryzacja**: portfel, procent inwestycji, poziomy SL/TP

**Technologie**:

* Python 3.x
* requests, pandas, TA-Lib
* Własny parser pliku konfiguracyjnego

**Struktura projektu**:

```
📁 tradingBot2_v0.0.2
📁 tradingBot2_v0.0.1
├── main.py
├── config.py
├── data_fetcher.py
├── indicators.py
├── strategy.py
├── simulator.py
├── trading.py
├── variables.conf
├── trade_log.csv
```

## Autor / Author

Igor Tomkowicz  •  📧 [npnpdev@gmail.com](mailto:npnpdev@gmail.com)  •  GitHub: [npnpdev](https://github.com/npnpdev)  •  LinkedIn: [igor-tomkowicz-a5760b358](https://www.linkedin.com/in/igor-tomkowicz-a5760b358/)

## Licencja / License

MIT License — see [LICENSE](LICENSE) for details.
