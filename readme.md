# Coin Balance and Activity Monitoring

This project is a Python script that monitors the balance and activity of coins from specified addresses using the Blockberry API.

## Features

- Retrieves the current balance for specified addresses.
- Monitors incoming coin activity.
- Displays information in a human-readable timestamp format.
- Handles API rate limits and errors gracefully.

## Prerequisites

- Python 3.x
- Required libraries:
  - `requests`
  - `json`
  - `logging`
  - `sys`

## Installation

1. Clone this repository.
2. Ensure you have an `address.txt` file containing the coin addresses you want to monitor, with one address per line.
3. Ensure you check the config.json and add your fav coin.
4. Replace api here in the script with your API key. You can get apikey from https://api.blockberry.one/
