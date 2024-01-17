import pandas as pd
from datetime import datetime

def top_up(topup_amount):
    # Read the balance.csv file
    df_balance = pd.read_csv('balance.csv')

    # Get the latest balance
    latest_balance = df_balance['balance'].iloc[-1]

    # Add the topup_amount to the latest balance
    new_balance = latest_balance + topup_amount

    # Create a new row with the new balance and today's date
    new_row = {'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'balance': round(new_balance, 2)}

    # Append the new row to the DataFrame
    df_balance.loc[len(df_balance)] = new_row

    # Write the DataFrame back to the balance.csv file
    df_balance.to_csv('balance.csv', index=False)


if __name__ == "__main__":
    top_up(50)
    print('Top up successful.')