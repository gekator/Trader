# 📈 Trader — Simple Backtesting Engine for Long/Short Trading Strategies

**Trader** is a lightweight, pure-Python backtesting engine designed for testing long and short trading strategies with realistic commission modeling (including MOEX-style fixed + percentage fees). It tracks your account balance, position size, unrealized PnL, and trade history — all in a clean, testable class-based interface.

Perfect for prototyping algorithmic strategies, educational purposes, or integrating into larger quant pipelines.

---

## ✨ Features

- **Long & Short support**: Open, close, and manage both long and short positions.
- **Realistic commissions**: Configurable percentage + fixed fee (e.g., `0.1% + 0 RUB`).
- **Account tracking**: Automatically logs `My_money`, `Stock_Cash`, and total `Account_money` over time.
- **Profit calculation**: Built-in methods for current PnL and total cash result.
- **Test-driven**: Comes with a full `unittest` suite for reliability.
- **No external dependencies** beyond `pandas` and `numpy`.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install pandas numpy
```

### 2. Basic usage example

```python
from Trader import Trader

# Initialize trader with 100,000 RUB, 0.1% commission + 0 fixed fee
trader = Trader(money=100_000, comis=[0.1, 0], printBool=True)

# Buy 5,000 units at price 10.0
trader.buy(orderVolume=5000, price=10.0)

# Sell 5,000 units at price 20.0 (close long)
trader.sell(orderVolume=5000, price=20.0)

# Get total profit
print("Total PnL:", trader.getCashResultFast(20.0))
```

### 3. Log account state over time

```python
trader.quant_money(price=15.0, date_now="2023-06-01")
trader.quant_money(price=18.0, date_now="2023-06-02")

# View full account history
print(trader.table)
```

---

## 🧪 Testing

The project includes a comprehensive test suite:

```bash
python -m pytest TestTrader.txt
# or
python TestTrader.txt
```

Tests cover:
- Commission calculation
- Long/short entry & exit
- Account value consistency
- Profit tracking accuracy

---

## 📂 Project Structure

```
.
├── Trader.txt          # Core Trader class (rename to Trader.py in real use)
├── TestTrader.txt      # Unit tests (rename to TestTrader.py)
└── CNY000000TOD_22-6-2022_18-7-2023_Test.txt  # Sample market data (CSV format expected)
```

> 💡 **Note**: The `.txt` extensions are likely placeholders. In a real repo, rename to `.py` and `.csv` accordingly.

---

## 💡 How It Works

- **`my_money`**: Cash not invested.
- **`posVolume`**: Current position (positive = long, negative = short).
- **`Account_money`**: Total equity = cash + value of open positions (adjusted for short logic).
- **`moneyOnStartDeal`**: Snapshot of account value at position entry — used to compute trade-level PnL.
- **Commissions**: Calculated as  
  `price * volume / 100 * comis[0] + comis[1]`  
  (e.g., `0.1% + 0 RUB` per trade).

Short positions are modeled using a "borrowed asset" approach: selling short reduces cash (you must post collateral), and profits come from buying back cheaper.

---

## 🛠️ Customization

- Adjust commission structure via the `comis=[percentage, fixed]` parameter.
- Disable verbose output with `printBool=False`.
- Use `getCashResultFast()` for real-time PnL without logging.
- Extend the class to integrate with live brokers or strategy logic.

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

---

## 🙌 Author

Created by **gekator** — for traders, by a trader.

---

> 🔍 **Tip**: Pair this engine with historical OHLC data (e.g., from MOEX or Binance) to backtest your strategies end-to-end!