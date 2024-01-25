import pandas as pd


def update_balance():
    # Load items.csv and balance.csv into pandas DataFrames
    items_df = pd.read_csv('items.csv')
    balance_df = pd.read_csv('balance.csv', parse_dates=['date'])

    # Manually parse the datetime column in items_df
    items_df['datetime'] = pd.to_datetime(items_df['datetime'], format='%Y-%m-%d %H:%M:%S')

    # Find the most recent date in items.csv
    most_recent_date = items_df['datetime'].max()

    # Filter items_df to get only rows with the most recent date
    recent_items = items_df[items_df['datetime'] == most_recent_date]

    # Calculate the total sum of prices on the most recent date
    total_sum = recent_items['price'].sum()

    # Deduct the total sum from the last row of the 'balance' column
    last_balance = balance_df['balance'].iloc[-1]
    new_balance = last_balance - total_sum

    # Create a new row for balance_df with the most recent date and the updated balance
    new_balance_row = {'date': most_recent_date, 'balance': round(new_balance, 2)}

    # Append the new row to balance_df
    balance_df.loc[len(balance_df)] = new_balance_row

    # Save the updated balance.csv
    balance_df.to_csv('balance.csv', index=False)

    print(f'Total sum of prices on {most_recent_date}: {total_sum}')
    print(f'Updated balance: {last_balance} - {total_sum} = {new_balance}')
    print('Updated balance.csv successfully.')


if __name__ == "__main__":
    update_balance()