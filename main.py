import requests
import time
import json
import logging
import sys

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

url_balance_template = "https://api.blockberry.one/sui/v1/accounts/{}/balance"
url_activity = "https://api.blockberry.one/sui/v1/accounts/0x0247d1a5066d73a78f228e2d2fef3e152f5f9486a09b76db34c8175a031a2ea1/activity"
headers = {
    "accept": "*/*",
    "x-api-key": "api here"
}

def get_balance(address, coins_to_monitor):
    url = url_balance_template.format(address)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        balances = {coin: 0 for coin in coins_to_monitor} 
        
        for coin in data:
            coin_symbol = coin.get("coinSymbol")
            if coin_symbol in balances:
                balances[coin_symbol] = coin.get("balance", 0) 

        return balances
    else:
        logging.error(f"Error fetching balance for {address}: {response.status_code}")
        return {coin: 0 for coin in coins_to_monitor} 

# Read config
def read_addresses(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config["coins"]

params = {
    "size": 1,
    "orderBy": "DESC"
}

# Variable to store the last timestamp
previous_timestamps = set()

# Read addresses and coins to monitor
addresses = read_addresses('address.txt')
coins_to_monitor = read_config('config.json')

loading_chars = ['|', '/', '-', '\\']  

try:
    while True:
        for address in addresses:
            balances = get_balance(address, coins_to_monitor)

            response = requests.get(url_activity, headers=headers, params=params)
            if response.status_code == 200:
                activities = response.json().get('content', [])
                if not activities:
                    for i in range(10):  
                        for char in loading_chars:
                            sys.stdout.write(f'\rLoading... {char}')
                            sys.stdout.flush()
                            time.sleep(0.1)
                    print('\r' + ' ' * 20 + '\r', end='')  
                else:
                    for activity in activities:
                        timestamp = activity.get('timestamp')
                        activity_type = activity.get('activityType')

                        if activity_type == "mine":
                            coins = activity.get('details', {}).get('detailsDto', {}).get('coins', [])

                            for coin in coins:
                                amount = coin.get('amount')
                                symbol = coin.get('symbol')

                                if amount and timestamp not in previous_timestamps:
                                    timestamp_in_seconds = timestamp / 1000
                                    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_in_seconds))

                                    balance = balances.get(symbol, 0)
                                    balance_formatted = f"{balance:,.2f}".replace(",", ".").replace(".", ",", 1)

                                    print(f"{formatted_time} - {symbol} masuk = {amount} - BALANCE {balance_formatted}")

                                    previous_timestamps.add(timestamp)

            elif response.status_code in (404, 500):
                logging.error(f"Error: {response.status_code} - {response.text}")
                time.sleep(5)
            elif response.status_code == 429:
                logging.warning("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)
            else:
                logging.error(f"Unexpected error: {response.status_code} - {response.text}")

        time.sleep(1)

except KeyboardInterrupt:
    logging.info("Script interrupted by user. Exiting...")
except Exception as e:
    logging.exception("An unexpected error occurred: %s", e)
