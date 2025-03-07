import pandas as pd
import matplotlib.pyplot as plt

def data_analyzer():
    print("Data Analyzer is running...")
    
    # Read the CSV file
    df = pd.read_csv('/Users/sebastianmraz/html_scraper/train_scraped_entries.csv')

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Set the 'date' column as the index
    df.set_index('date', inplace=True)

    # Sort the data by date
    df.sort_index(inplace=True)

    # Plot the time series data
    df.plot()
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Time Series Data')
    plt.show()

if __name__ == "__main__":
    data_analyzer()