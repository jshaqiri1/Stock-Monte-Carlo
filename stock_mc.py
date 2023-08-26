import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Download stock data
def download_data(ticker):
    df = yf.download(ticker)
    return df

# Calculate returns
def calculate_returns(df):
    returns = np.log(1+df['Adj Close'].pct_change())
    mu, sigma = returns.mean(), returns.std()
    return mu, sigma

# Simulate prices
def simulate_prices(initial, mu, sigma):
    sim_rets = np.random.normal(mu, sigma, 252)
    sim_prices = initial * (sim_rets+1).cumprod()
    return sim_prices

# Plot prices
def plot_prices(initial, sim_prices_list):
    fig, ax = plt.subplots()
    plt.axhline(initial, c='k')
    for sim_prices in sim_prices_list:
        plt.plot(sim_prices)
    plt.title("Simulated Prices")
    plt.xlabel("Trading Days")
    plt.ylabel("Price ($)")
    return fig

# Main function
def main():
    # Simulation settings
    ticker = st.sidebar.text_input("Enter Ticker Symbol", "MSFT")
    num_simulations = st.sidebar.slider("Number of Simulations", 1, 100, 10)
    
    # Page title
    st.title(f"Stock Price Simulation ({ticker})")

    # Sidebar
    st.sidebar.title("Simulation Settings")



    st.sidebar.write("""
    ## Description
    This tool simulates future stock prices through a Monte-Carlo analysis using historical price data to calculates the expected returns, standard deviation
    and volatility. It then simulates future prices based on those parameters.
    The tool can simulate multiple future price scenarios, allowing users to assess the potential
    range of future prices and plan their investment strategy accordingly.
    """)

    
    # Download data
    df = download_data(ticker)
    mu, sigma = calculate_returns(df)
    initial = df['Adj Close'].iloc[-1]


    # Run simulations
    sim_prices_list = []
    for i in range(num_simulations):
        sim_prices = simulate_prices(initial, mu, sigma)
        sim_prices_list.append(sim_prices)
    
    # Plot all simulations
    fig = plot_prices(initial, sim_prices_list)
    st.pyplot(fig)

if __name__ == '__main__':
    main()
