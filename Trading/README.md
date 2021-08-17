## Overview

This is a stop-loss bot for the Terra blockchain. It will convert Luna to UST if the price of Luna drops below a user specified stop-loss price.
It will be extended to support additional currencies and trading functionality.

## Prerequisites

### Software
1. Install [git](https://git-scm.com/)
2. Install [python](https://www.python.org/downloads/)

### Slack

1. Slack account
2. Slack workspace where the bot will be installed

## Installation Instructions

Note: This project has only been tested on a machine running Ubuntu Linux 20.04

1. Set up a slack bot (instructions are similar to those found [here](../LiquiditySnipping/README.md))
2. Run `pip install -r requirements.txt` in a terminal
3. Run `python main.py` in a terminal

## License

MIT