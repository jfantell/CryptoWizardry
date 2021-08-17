from terra_sdk.client.lcd.api.bank import BankAPI
from terra_sdk.client.lcd.wallet import Wallet

# Get balance of luna in provided wallet
def getLunaBalance(wallet : Wallet, bank: BankAPI) -> int:
    coins = bank.balance(wallet.key.acc_address)
    for coin in coins:
        if coin.denom == 'uluna':
            return int(coin.amount)
    return 0