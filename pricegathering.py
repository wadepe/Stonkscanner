import robin_stocks as r
import csv
import time

# Replace these with your Robinhood login credentials
username = 'wadepe@yahoo.com'
password = 'Robinhood1!'

# Log in to Robinhood
login = r.robinhood.authentication.login(username, password)

# Function to get Bitcoin bid price, ask price, and volume
def get_bitcoin_data():
    bitcoin_data = r.robinhood.crypto.get_crypto_quote('BTC') # Get Bitcoin data
    bid_price = bitcoin_data['bid_price']
    ask_price = bitcoin_data['ask_price']
    mark_price = bitcoin_data['mark_price']
    return bid_price, ask_price, mark_price

# Create a CSV file and write headers if the file doesn't exist
with open('bitcoin_data.csv', 'a', newline='') as csvfile:
    fieldnames = ['Time', 'Bid Price', 'Ask Price', 'Mark Price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # If the file is empty, write headers
    if csvfile.tell() == 0:
        writer.writeheader()
    
    while True:
        ts = time.time()
        bid, ask, mark = get_bitcoin_data() # Get Bitcoin data
        writer.writerow({'Time' : ts, 'Bid Price': bid, 'Ask Price': ask, 'Mark Price' : mark}) # Write data to CSV
        print({'Time' : ts, 'Bid Price': bid, 'Ask Price': ask, 'Mark Price' : mark})
        time.sleep(5) # Wait for 5 seconds
