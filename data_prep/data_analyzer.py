import pandas as pd
import matplotlib.pyplot as plt

def data_analyzer():
    print("Data Analyzer is running...")
    
    # Read the CSV file
    df = pd.read_csv('/Users/sebastianmraz/html_scraper/legislation/unique_dates_counts.csv')
    
    # Ensure the 'Date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Set the 'Date' column as the index
    df.set_index('date', inplace=True)
    
    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot the time series data
    axs[0].plot(df.index, df['count'], label='count')
    axs[0].set_xlabel('date')
    axs[0].set_ylabel('value')
    axs[0].set_title('Differences Time Series Data')
    axs[0].legend()
    
    # Calculate the cumulative sum of 'count'
    df['cumulative_sum'] = df['count'].cumsum()
    
    # Plot the cumulative sum
    axs[1].plot(df.index, df['cumulative_sum'], label='cumulative sum')
    axs[1].set_xlabel('date')
    axs[1].set_ylabel('cumulative sum')
    axs[1].set_title('Cumulative Sum of Count Over Time')
    axs[1].legend()
    
    # Adjust layout
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data_analyzer()