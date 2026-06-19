from src.data_loader import PriceDataHandler
from src.markov import MarkovChain

if __name__ == "__main__":
    symbol = "ES=F"
    start_date = "2000-01-01"
    end_date = "2025-12-31"
    price_data_handler = PriceDataHandler(
        symbol=symbol, start_date=start_date, end_date=end_date
    )
    price_data_handler.fetch_data()
    price_data_handler.calculate_features()
    markov_chain = MarkovChain()
    markov_chain.fit(price_data_handler.prices)
    breakpoint()