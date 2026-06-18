````markdown
# 🧠 simple-bias-markov-chain

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-learning_project-brightgreen)
![Markets](https://img.shields.io/badge/markets-continuous_futures-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A simple but practical learning project for using **Markov chains** to study market regimes and build a basic **daily bias framework**.

The goal is not to predict the market perfectly.

The goal is to answer a better question:

> Given the current market state, what type of market state tends to come next?

This project uses daily data from **Yahoo Finance** and can be applied to any continuous futures contract available there, such as `ES=F`, `NQ=F`, `CL=F`, `GC=F`, and more.

---

## 🎯 Project Purpose

This repository was created to learn how simple Markov chains can be used in trading research.

It is especially useful for traders interested in:

- 📊 Auction Market Theory
- 🧩 Market regimes
- 📈 Daily bias generation
- 🔁 Markov chains
- 🧠 Quantitative thinking
- ⚡ Futures markets
- 🔍 Research before execution

The project intentionally keeps the model simple.

Before jumping into complex models like Hidden Markov Models, order-flow features, volume profile, or machine learning, this project focuses on the core idea:

> Markets move through states, and those states have transition probabilities.

---

## 🧠 Core Idea

Each trading day is classified into one of a few simple market regimes:

- `UP_TREND`
- `DOWN_TREND`
- `BALANCE`
- `VOLATILE`

Then the project calculates how often one state transitions into another.

For example:

```text
If today is BALANCE,
how often is tomorrow also BALANCE?

If today is UP_TREND,
how often does the next day continue as UP_TREND?

If today is VOLATILE,
does the market usually calm down or stay volatile?
```

This creates a simple **transition matrix** that can be used as a basic market-bias tool.

---

## 🔁 What Is a Markov Chain?

A Markov chain is a model where the next state depends only on the current state.

In this project, that means:

```text
Tomorrow's market regime depends on today's market regime.
```

Example:

```text
BALANCE → BALANCE
BALANCE → UP_TREND
BALANCE → DOWN_TREND
BALANCE → VOLATILE
```

The model counts these transitions historically and converts them into probabilities.

---

## 📦 Supported Markets

This project can be used with any Yahoo Finance continuous futures symbol.

| Market                | Yahoo Finance Symbol |
| --------------------- | -------------------- |
| E-mini S&P 500        | `ES=F`               |
| E-mini Nasdaq 100     | `NQ=F`               |
| Dow Futures           | `YM=F`               |
| Russell 2000 Futures  | `RTY=F`              |
| Crude Oil             | `CL=F`               |
| Gold                  | `GC=F`               |
| Silver                | `SI=F`               |
| Natural Gas           | `NG=F`               |
| 10-Year Treasury Note | `ZN=F`               |

Default example:

```python
symbol = "ES=F"
```

---

## ⚙️ How It Works

The workflow is simple:

```text
1. Download daily data from Yahoo Finance
2. Calculate daily features
3. Classify each day into a regime
4. Build a Markov transition matrix
5. Use the probabilities as a bias/context tool
```

---

## 🧪 Example Regime Logic

Each day is classified using simple features such as:

- Daily return
- Daily range
- Close location inside the day’s range
- Volatility relative to recent average range

Example classification logic:

```text
Strong positive return + close near high  → UP_TREND
Strong negative return + close near low   → DOWN_TREND
Large range with no clear direction       → VOLATILE
Everything else                           → BALANCE
```

This logic is intentionally simple and should be adjusted during research.

---

## 📊 Example Transition Matrix

The output may look something like this:

```text
Next State       BALANCE   UP_TREND   DOWN_TREND   VOLATILE
Current State
BALANCE           54.2%      18.5%       16.1%       11.2%
UP_TREND          43.8%      28.4%       12.7%       15.1%
DOWN_TREND        45.3%      13.9%       25.6%       15.2%
VOLATILE          48.6%      17.4%       18.2%       15.8%
```

This can then be translated into a simple trading context.

Example:

```text
If BALANCE has the highest probability:
    Avoid chasing breakouts from the middle of the range.

If UP_TREND continuation probability is elevated:
    Give more weight to long pullback setups.

If VOLATILE probability is elevated:
    Reduce size and wait for better trade location.
```

---

## 📈 Example Use Case

Suppose yesterday was classified as:

```text
BALANCE
```

And the model shows:

```text
After BALANCE:
- BALANCE: 54%
- UP_TREND: 18%
- DOWN_TREND: 16%
- VOLATILE: 12%
```

Then the daily bias is not necessarily bullish or bearish.

Instead, the useful takeaway is:

```text
The market has a higher probability of remaining rotational.
Be careful chasing moves.
Prioritize better location.
Wait for confirmation.
```

For an order-flow trader, this can help decide whether to:

- Fade extremes
- Trade continuation
- Avoid the middle
- Reduce size
- Wait for stronger confirmation

---

## 🗂️ Project Structure

```text
simple-bias-markov-chain/
│
├── data/                 # Optional local data storage
├── notebooks/            # Research notebooks
├── src/                  # Core Python code
│   ├── data_loader.py
│   ├── features.py
│   ├── regimes.py
│   └── markov_chain.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/simple-bias-markov-chain.git
cd simple-bias-markov-chain
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate
```

```bash
# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📚 Requirements

Basic dependencies:

```text
pandas
numpy
yfinance
matplotlib
```

Optional dependencies:

```text
jupyter
seaborn
```

---

## ▶️ Basic Usage

Run the main script:

```bash
python main.py
```

Or open the notebook:

```bash
jupyter notebook
```

Change the symbol to test another market:

```python
symbol = "ES=F"
```

For example:

```python
symbol = "NQ=F"
```

or:

```python
symbol = "CL=F"
```

---

## 🔍 Research Questions

This project can help explore questions like:

- What usually follows a balanced day?
- Do trend days tend to continue or mean revert?
- Does volatility cluster from one day to the next?
- Are some futures markets more rotational than others?
- Can a simple regime model improve daily bias preparation?
- Do certain setups perform better after specific regimes?

---

## 🧱 Possible Extensions

Future improvements may include:

- Add VIX data
- Add NQ vs ES relative strength
- Add overnight gap features
- Add RTH vs ETH session separation
- Add prior day high, low, close, and range context
- Add volume-profile levels such as VAH, VAL, and POC
- Add order-flow features such as delta and volume imbalance
- Upgrade to Hidden Markov Models
- Backtest setup performance by regime

---

## ⚠️ Important Notes

This project is for **education and research only**.

Yahoo Finance data is useful for learning and prototyping, but it may not be clean enough for professional-grade futures research.

For more serious futures research, consider using dedicated market data providers with clean historical futures data.

---

## 🧠 Why This Project Exists

Many traders create daily bias using narratives, screenshots, or discretionary pattern recognition.

This project tries to make the process more structured and testable.

Instead of asking:

```text
What do I think the market will do tomorrow?
```

It asks:

```text
What has the market historically tended to do after this type of day?
```

That shift is the entire point of the project.

The model does not need to be perfect to be useful.

Even a simple regime model can help a trader avoid using the wrong playbook on the wrong type of day.

---

## 📌 Disclaimer

This repository is for educational purposes only.

Nothing in this project should be considered financial advice, trading advice, or a recommendation to buy or sell any financial instrument.

Trading futures involves substantial risk.

---

## 📄 License

This project is licensed under the MIT License.
````
