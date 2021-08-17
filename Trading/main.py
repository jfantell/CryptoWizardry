# Load environmental variables
from dotenv import load_dotenv
load_dotenv()

# Set up logging
from wizardtrading.loggingUtils import LogFactory
logger = LogFactory.getLogger(__name__)

# Other imports
from wizardtrading.utils import getLunaBalance
from wizardtrading.transaction import sendTransaction
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.market.msgs import MsgSwap
from terra_sdk.core.coin import Coin
from terra_sdk.client.lcd.api.market import MarketAPI
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd.api.oracle import OracleAPI
from terra_sdk.client.lcd.api.bank import BankAPI
import os
import time
from wizardtrading.db import Database
from slack_bolt import App

# Set up slack bot
bot = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Set up DB
# DB = Database()

# Set up LCD and Wallet
MNEMONIC = os.getenv('TERRA_MNEMONIC')

lcd = LCDClient(chain_id="columbus-4", url="https://lcd.terra.dev")
mk = MnemonicKey(mnemonic=MNEMONIC)
wallet = lcd.wallet(mk)

# Additional setup
bank = BankAPI(lcd)
oracle = OracleAPI(lcd)
market = MarketAPI(lcd)
# When the price of luna drops to $18 USD, swap Luna for UST to minimize profit loss
LUNA_SELL_PRICE_IN_USD = 18
# Query blockchain every 30 seconds
SLEEP_SEC=30
# Safety Check: Make sure that the swap price remains below the stop-loss price for 2 queries
# within close temporal proximity before actually initiating the swap
timeSinceStopLossTriggered = 0

while True:
    # Get balance of luna from personal wallet
    luna_balanace = getLunaBalance(wallet, bank)
    if luna_balanace <= 0:
        logger.info(f"Wallet Luna Balance Less Than 0")
        continue
    logger.info(f"Wallet Luna Balance: {luna_balanace}")
    
    # Get the swap price of luna from blockchain
    luna = Coin("uluna", luna_balanace)
    luna_market_value = market.swap_rate(luna, "uusd").amount
    logger.info(f"Market Swap Price For Provided Luna Balance: {luna_market_value}")
    
    # Stop loss sell signal
    stop_loss_value = LUNA_SELL_PRICE_IN_USD * luna_balanace
    if luna_market_value < stop_loss_value:
        logger.warning(f"CURRENT LUNA MARKET VALUE {luna_market_value}uusd LESS THAN STOP-LOSS VALUE {stop_loss_value}uusd")
        # Start timer when swap price first drops below stop-loss price
        if timeSinceStopLossTriggered == 0:
            timeSinceStopLossTriggered = time.time()
            continue
        # Compute elapsed time since swap price dropped below stop-loss price
        timeElapsed = time.time() - timeSinceStopLossTriggered
        # If elapsed time is too large, do not initiate the swap, perhaps a fluke
        if timeElapsed > 3*SLEEP_SEC:
            timeSinceStopLossTriggered = 0
        else:
            logger.warning("== INITIATING SWAP ==")
            sendTransaction(wallet, MsgSwap(wallet.key.acc_address, luna, "uusd"), lcd, bot)
    time.sleep(SLEEP_SEC)