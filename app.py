import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

# Define the various strategies
class SMAStrategy(Strategy):
    n1 = 40
    n2 = 100

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

class EMAStrategy(Strategy):
    n1 = 12
    n2 = 26

    def init(self):
        self.ema1 = self.I(lambda x: pd.Series(x).ewm(span=self.n1, adjust=False).mean(), self.data.Close)
        self.ema2 = self.I(lambda x: pd.Series(x).ewm(span=self.n2, adjust=False).mean(), self.data.Close)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.sell()

class BollingerBandsStrategy(Strategy):
    period = 20
    devfactor = 2

    def init(self):
        self.middle = self.I(lambda x: pd.Series(x).rolling(self.period).mean(), self.data.Close)
        self.std = self.I(lambda x: pd.Series(x).rolling(self.period).std(), self.data.Close)
        self.upper = self.middle + (self.devfactor * self.std)
        self.lower = self.middle - (self.devfactor * self.std)

    def next(self):
        if self.data.Close < self.lower:
            self.buy()
        elif self.data.Close > self.upper:
            self.sell()

class RSIStrategy(Strategy):
    period = 14
    overbought = 70
    oversold = 30

    def init(self):
        close = pd.Series(self.data.Close)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).ewm(span=self.period, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(span=self.period, adjust=False).mean()
        rs = gain / loss
        self.rsi = self.I(lambda x: 100 - (100 / (1 + rs)), self.data.Close)

    def next(self):
        if self.rsi < self.oversold:
            self.buy()
        elif self.rsi > self.overbought:
            self.sell()

class MACDStrategy(Strategy):
    def init(self):
        self.macd_line = self.I(lambda x: pd.Series(x).ewm(span=12, adjust=False).mean() - pd.Series(x).ewm(span=26, adjust=False).mean(), self.data.Close)
        self.signal_line = self.I(lambda x: pd.Series(x).ewm(span=9, adjust=False).mean(), self.macd_line)

    def next(self):
        if crossover(self.macd_line, self.signal_line):
            self.buy()
        elif crossover(self.signal_line, self.macd_line):
            self.sell()

class BuyHoldStrategy(Strategy):
    def init(self):
        self.buy()

    def next(self):
        pass

# Function to load data
def load_data(file):
    data = pd.read_csv(file, parse_dates=['Date'], index_col='Date')
    return data

# Function to plot results
def plot_backtest_results(bt):
    fig = bt.plot()
    st.pyplot(fig)

# Main function
def main():
    st.title('Trading Strategy Backtesting App')

    # File upload
    st.sidebar.title('Upload Your Stock Data')
    uploaded_file = st.sidebar.file_uploader('Choose a file')

    # Input initial capital
    st.sidebar.title('Initial Capital')
    initial_capital = st.sidebar.number_input('Enter initial capital', min_value=1000, value=100000, step=1000)

    st.sidebar.title('Select Trading Strategy')
    strategy = st.sidebar.selectbox('Strategy', ['SMA', 'EMA', 'Bollinger Bands', 'RSI', 'MACD', 'Buy and Hold'])

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write('**Stock Data**')
        st.write(data.head())

        # Initialize strategy
        if strategy == 'SMA':
            st.sidebar.subheader('SMA Strategy Parameters')
            short_window = st.sidebar.number_input('Short Window', min_value=1, max_value=200, value=40)
            long_window = st.sidebar.number_input('Long Window', min_value=1, max_value=200, value=100)
            bt = Backtest(data, SMAStrategy, cash=initial_capital, trade_on_close=True)
            SMAStrategy.n1 = short_window
            SMAStrategy.n2 = long_window
        elif strategy == 'EMA':
            st.sidebar.subheader('EMA Strategy Parameters')
            short_window = st.sidebar.number_input('Short Window', min_value=1, max_value=200, value=12)
            long_window = st.sidebar.number_input('Long Window', min_value=1, max_value=200, value=26)
            bt = Backtest(data, EMAStrategy, cash=initial_capital, trade_on_close=True)
            EMAStrategy.n1 = short_window
            EMAStrategy.n2 = long_window
        elif strategy == 'Bollinger Bands':
            st.sidebar.subheader('Bollinger Bands Strategy Parameters')
            period = st.sidebar.number_input('Period', min_value=1, max_value=200, value=20)
            devfactor = st.sidebar.number_input('Deviation Factor', min_value=1, max_value=5, value=2)
            bt = Backtest(data, BollingerBandsStrategy, cash=initial_capital, trade_on_close=True)
            BollingerBandsStrategy.period = period
            BollingerBandsStrategy.devfactor = devfactor
        elif strategy == 'RSI':
            st.sidebar.subheader('RSI Strategy Parameters')
            period = st.sidebar.number_input('Period', min_value=1, max_value=200, value=14)
            overbought = st.sidebar.number_input('Overbought', min_value=50, max_value=100, value=70)
            oversold = st.sidebar.number_input('Oversold', min_value=0, max_value=50, value=30)
            bt = Backtest(data, RSIStrategy, cash=initial_capital, trade_on_close=True)
            RSIStrategy.period = period
            RSIStrategy.overbought = overbought
            RSIStrategy.oversold = oversold
        elif strategy == 'MACD':
            bt = Backtest(data, MACDStrategy, cash=initial_capital, trade_on_close=True)
        elif strategy == 'Buy and Hold':
            bt = Backtest(data, BuyHoldStrategy, cash=initial_capital, trade_on_close=True)

        # Run backtest
        st.subheader('Running Backtest...')
        stats = bt.run()

        # Plot results
        st.subheader('Backtest Results')
        st.write(stats)

if __name__ == "__main__":
    main()
