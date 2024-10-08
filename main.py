import requests
import time
import json
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

url_balance_template = "https://api.blockberry.one/sui/v1/accounts/{}/balance"
url_activity_template = "https://api.blockberry.one/sui/v1/accounts/{}/activity"
headers = {
    "accept": "*/*",
    "x-api-key": "paste api here"
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

def get_activity(address):
    url = url_activity_template.format(address)
    params = {
        "size": 1,
        "orderBy": "DESC"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get('content', [])
    else:
        logging.error(f"Error fetching activity for {address}: {response.status_code}")
        return []

def read_addresses(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config["coins"]

def shorten_address(address):
    if len(address) > 15:
        return f"{address[:8]}...{address[-7:]}"
    return address

def main():
    addresses = read_addresses('address.txt')
    coins_to_monitor = read_config('config.json')

    previous_timestamps = set()
    initial_balances = {}

    for address in addresses:
        balances = get_balance(address, coins_to_monitor)
        initial_balances[address] = balances
        print(f"Checking {shorten_address(address)}: {balances}")

    try:
        while True:
            any_activity_found = False

            for address in addresses:
                activities = get_activity(address)
                new_activity_found = False

                for activity in activities:
                    activity_type = activity.get('activityType')

                    if activity_type == "mine":
                        new_activity_found = True
                        any_activity_found = True

                        coins = activity.get('details', {}).get('detailsDto', {}).get('coins', [])

                        for coin in coins:
                            amount = coin.get('amount')
                            symbol = coin.get('symbol')
                            timestamp = activity.get('timestamp')

                            if amount and timestamp not in previous_timestamps:
                                new_balances = get_balance(address, coins_to_monitor)
                                if new_balances != initial_balances[address]:
                                    initial_balances[address] = new_balances

                                timestamp_in_seconds = timestamp / 1000
                                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_in_seconds))

                                balance = initial_balances[address].get(symbol, 0)
                                balance_formatted = f"{balance:,.2f}".replace(",", ".").replace(".", ",", 1)

                                print(f"{formatted_time} - {shorten_address(address)} - {symbol} masuk = {amount} - BALANCE {balance_formatted}")
                                previous_timestamps.add(timestamp)
                                time.sleep(1)
                        
    
    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting...")
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)

if __name__ == "__main__":
    main()
