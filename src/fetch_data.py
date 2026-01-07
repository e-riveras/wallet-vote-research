import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import os

def fetch_economic_data(start_date="1970-01-01"):
    """
    Fetches economic indicators from FRED and resamples to monthly.
    """
    print("Fetching economic data from FRED...")
    # WILL5000PRFC is a good long-term proxy for the S&P 500 on FRED
    series = {
        'CPIAUCSL': 'inflation_cpi',
        'UNRATE': 'unemployment_rate',
        'GASREGW': 'gas_prices',
        'WILL5000PRFC': 'stock_market'
    }
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    df_list = []
    for code, name in series.items():
        try:
            data = web.DataReader(code, 'fred', start_date, end_date)
            # CRITICAL: Resample to Month Start ('MS') to align disparate frequencies
            # We take the mean for the month to represent the general state
            data = data.resample('MS').mean()
            data.columns = [name]
            df_list.append(data)
        except Exception as e:
            print(f"Error fetching {code}: {e}")
            
    # Combine all series - they are now all aligned on Month Start
    economics = pd.concat(df_list, axis=1)
    return economics

def fetch_approval_data():
    """
    Fetches historical presidential approval data.
    Using a curated dataset from the American Presidency Project or similar reliable source.
    For this project, we'll use a reliable GitHub-hosted cleaned version of Gallup data.
    """
    print("Fetching approval data...")
    # This is a common reliable URL for historical approval ratings (Gallup data aggregated)
    url = "https://raw.githubusercontent.com/lorenzo-ruffino/approval_rate_usa_president/main/historical_approval_polls.csv"
    try:
        df = pd.read_csv(url)
        # Convert date and filter
        # The new dataset uses 'poll_end' for the date of the poll
        df['date'] = pd.to_datetime(df['poll_end'])
        # We'll take the average approval per month to match economic data
        df = df.set_index('date')
        # The column is named 'approval' in this dataset
        monthly_approval = df[['approval']].resample('MS').mean()
        monthly_approval.columns = ['approval_rating']
        return monthly_approval
    except Exception as e:
        print(f"Error fetching approval data: {e}")
        return None

def main():
    os.makedirs('data', exist_ok=True)
    
    # Fetch data
    econ_df = fetch_economic_data()
    approval_df = fetch_approval_data()
    
    if econ_df is not None and approval_df is not None:
        # Merge datasets on index (Date)
        # Economic data is usually monthly (MS - Month Start)
        final_df = econ_df.join(approval_df, how='inner')
        
        output_path = 'data/processed_data.csv'
        final_df.to_csv(output_path)
        print(f"Data saved successfully to {output_path}")
    else:
        print("Data fetching failed.")

if __name__ == "__main__":
    main()
