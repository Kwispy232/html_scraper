import pandas as pd

def data_prep():
    df = pd.read_csv('/Users/sebastianmraz/html_scraper/legislation/scraped_legislation.csv')
    dates = pd.to_datetime(df['datum'], format='%d.%m.%Y')
    unique_dates = pd.date_range(start=dates.min(), end=dates.max()).tolist()
    print(f"Unique dates: {len(unique_dates)}")
    data = []
    for date in unique_dates:
        count = dates[dates == date].count()
        data.append({'date': date, 'count': count})
    
    result_df = pd.DataFrame(data)
    result_df.to_csv('/Users/sebastianmraz/html_scraper/unique_dates_counts.csv', index=False)
    print(f"CSV file created with {len(unique_dates)} unique dates.")

if __name__ == "__main__":
    data_prep()