# 🧠 simple-bias-markov-chain

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-learning_project-brightgreen)
![Markets](https://img.shields.io/badge/markets-continuous_futures-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A simple but practical learning project for using **Markov chains** to study market regimes and build a basic **daily bias framework** for futures.

The goal is not to predict the market perfectly.

The goal is to answer a better question:

> Given the current market state, what type of market state has historically tended to come next?

This project currently uses daily data from **Yahoo Finance** and can be applied to any continuous futures contract available there, such as `ES=F`, `NQ=F`, `CL=F`, `GC=F`, and more.

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

If today is DOWN_TREND,
does the market tend to continue lower, reverse upward, or return to balance?

If today is VOLATILE,
does the market usually calm down or remain volatile?
```

This creates a simple **transition matrix** that can be used as a basic market-bias and auction-context tool.

---

## 🔁 What Is a Markov Chain?

A Markov chain is a model where the next state depends only on the current state.

In this project, that means:

```text
Tomorrow's market regime is studied as a function of today's market regime.
```

Example:

```text
BALANCE -> BALANCE
BALANCE -> UP_TREND
BALANCE -> DOWN_TREND
BALANCE -> VOLATILE
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
4. Build a Markov transition-count matrix
5. Convert transition counts into transition probabilities
6. Compare transition probabilities against the baseline state distribution
7. Use the result as bias/context, not as a standalone trading signal
```

---

## 🧪 Current Feature Logic

The project currently calculates:

- Previous close
- Daily return
- Daily range percentage
- Close location inside the day's range
- True range
- ATR(14)
- True range as a percentage of previous close
- ATR(14) as a percentage of previous close

The current regime logic is:

```text
Strong positive return + close near high -> UP_TREND
Strong negative return + close near low  -> DOWN_TREND
Large range without clear direction      -> VOLATILE
Everything else                          -> BALANCE
```

Default thresholds in `src/markov.py`:

```text
return_threshold        = 0.003
close_location_upper    = 0.60
close_location_lower    = 0.40
volatility_multiplier   = 1.5
```

This logic is intentionally simple and should be adjusted during research.

---

## 📊 Example Transition Matrix

The output may look something like this:

```text
next_state   BALANCE  DOWN_TREND  UP_TREND  VOLATILE
state
BALANCE       0.4367      0.2204    0.3247    0.0182
DOWN_TREND    0.3073      0.2639    0.3941    0.0347
UP_TREND      0.4389      0.2228    0.3224    0.0159
VOLATILE      0.4342      0.1711    0.3553    0.0395
```

This can then be translated into a simple trading context.

Example:

```text
If UP_TREND continuation probability is below baseline:
    Avoid blindly chasing upside continuation after a strong up day.

If DOWN_TREND -> UP_TREND is above baseline:
    Be alert for a possible bounce or downside rejection the next day.

If VOLATILE has very few observations:
    Treat that row as unstable until more data is available.
```

---

## 📐 Baseline And Edge

The transition matrix is more useful when compared with the unconditional baseline.

The baseline answers:

```text
How often does each state happen in general?
```

Example:

```python
df = markov_chain.classify_states(price_data_handler.prices)
baseline = df["state"].value_counts(normalize=True)
```

The edge table answers:

```text
After a given state, is the next state more or less likely than usual?
```

Example:

```python
edge = markov_chain.transition_probs.subtract(baseline, axis=1)
```

Interpretation:

```text
Positive edge -> next state is more likely than usual after the current state
Negative edge -> next state is less likely than usual after the current state
Near zero     -> current state may not add much information
```

This helps separate real transition information from the market's normal state distribution.

---

## 📈 Example Use Case

Suppose yesterday was classified as:

```text
DOWN_TREND
```

And the model shows:

```text
After DOWN_TREND:
- BALANCE:    below baseline
- UP_TREND:   above baseline
- DOWN_TREND: slightly above baseline
- VOLATILE:   slightly above baseline
```

Then the daily bias is not simply bullish or bearish.

Instead, the useful takeaway is:

```text
The market may be less likely to return to quiet balance immediately.
Prepare for either a bounce/reversal or continued directional auction.
Use price acceptance/rejection around key levels before acting.
```

For an auction-market trader, this can help decide whether to:

- Fade poor location
- Trade continuation only after acceptance
- Avoid chasing from the middle
- Reduce size when context is unclear
- Wait for confirmation around prior value, prior range, or session extremes

---

## 🧭 Auction Market Theory Direction

The current model is candle-based and intentionally simple.

For stronger Auction Market Theory research, future states should become more value-based.

Useful future state ideas:

- `BALANCE_INSIDE_VALUE`
- `UP_ACCEPTANCE`
- `DOWN_ACCEPTANCE`
- `UP_REJECTION`
- `DOWN_REJECTION`
- `FAILED_BREAKOUT`
- `VALUE_HIGHER`
- `VALUE_LOWER`
- `VALUE_OVERLAPPING`
- `VOLATILE_EXPANSION`

Important AMT features to add later:

- Prior day high, low, close, and range
- Prior value area high, value area low, and point of control
- Opening location relative to prior value
- Closing location relative to prior value
- Value migration higher, lower, or overlapping
- Multi-day balance highs and lows
- Failed breaks above or below balance
- RTH versus ETH session separation

The long-term goal is for the Markov chain to study auction behavior such as:

```text
If price opens above prior value, does it accept higher or reject back inside?
If value migrates higher today, does value keep migrating higher tomorrow?
If price breaks a multi-day balance, does it continue or fail?
```

---

## 🗂️ Project Structure

```text
simple-bias-markov-chain/
│
├── data/                 # Optional local data storage
├── src/                  # Core Python code
│   ├── data_loader.py    # Downloads data and calculates features
│   └── markov.py         # Classifies states and builds transition matrices
├── main.py               # Example script / debugger entry point
├── requirements.txt      # Python dependencies
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

---

## ▶️ Basic Usage

Run the main script:

```bash
python main.py
```

The current `main.py` downloads data, calculates features, fits the Markov model, and enters the debugger.

Useful debugger checks:

```python
markov_chain.transition_counts
markov_chain.transition_probs
```

To calculate the baseline and edge:

```python
df = markov_chain.classify_states(price_data_handler.prices)
baseline = df["state"].value_counts(normalize=True)
edge = markov_chain.transition_probs.subtract(baseline, axis=1)
```

Change the symbol or date range to test another market or period:

```python
symbol = "ES=F"
start_date = "2012-01-01"
end_date = "2025-12-31"
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
- Does a current state still matter after comparing it to the baseline distribution?
- Are the same transitions stable across different market periods?

---

## 🧱 Possible Extensions

Future improvements may include:

- Add VIX data
- Add NQ versus ES relative strength
- Add overnight gap features
- Add RTH versus ETH session separation
- Add prior day high, low, close, and range context
- Add value-area levels such as VAH, VAL, and POC
- Add value migration states
- Add multi-day balance and failed-breakout states
- Add order-flow features such as delta and volume imbalance
- Add train/test or walk-forward validation
- Upgrade to Hidden Markov Models
- Backtest setup performance by regime

---

## ⚠️ Important Notes

This project is for **education and research only**.

Yahoo Finance data is useful for learning and prototyping, but it may not be clean enough for professional-grade futures research.

For serious futures research, consider using dedicated market data providers with clean historical futures data, proper continuous-contract handling, and intraday/RTH session support.

The transition matrix should not be treated as a direct buy/sell signal.

It is better used as a context filter:

```text
Which auction playbook deserves more attention after today's state?
```

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
