# Coin Balance and Activity Monitoring

This project is a Python script that monitors the balance and activity of coins from specified addresses using the Blockberry API.

## Features

- Retrieves the current balance for specified addresses.
- Monitors incoming coin activity.
- Displays information in a human-readable timestamp format.
- Handles API rate limits and errors gracefully.
- Shows a loading animation when no new activities are detected.

## Prerequisites

- Python 3.x
- Required libraries:
  - `requests`
  - `json`
  - `logging`
  - `sys`

## Installation

1. Clone this repository or download the `script.py` file.
2. Ensure you have an `address.txt` file containing the coin addresses you want to monitor, with one address per line.
