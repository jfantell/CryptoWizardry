from terra_sdk.client.lcd.lcdclient import LCDClient
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank import MsgSend
from terra_sdk.client.lcd.wallet import Wallet
from terra_sdk.core.broadcast import BlockTxBroadcastResult
from wizardtrading.loggingUtils import LogFactory
from slack_bolt import App


logger = LogFactory.getLogger(__name__)

def sendTransaction(wallet : Wallet, msg : MsgSend, lcd: LCDClient, app : App) -> BlockTxBroadcastResult:
    # Send transaction to blockchain and log result
    tx = wallet.create_and_sign_tx(
        msgs=[msg],
        memo="test transaction!",
        fee=StdFee(200000, "1000000uusd")
    )
    result = lcd.tx.broadcast(tx)
    logger.info(result)
    
    # Send transaction status to Slack via Slack Bot
    transaction_status = "** Swap Transaction Succeeded"
    if result.code:
        transaction_status =  "**Swap Transaction Failed**"

    app.client.chat_postMessage(
        channel="cryptowizardry",
        blocks=[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": transaction_status
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": str(result)
            }
        }]
    )

    # If error occurred with transaction, exit the program
    if result.code:
        raise Exception(f"Swap Transaction Failed: {result}")
    return result