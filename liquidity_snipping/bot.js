require('dotenv').config();
const { addresses } = require('../addresses');
const { abis } = require('../abis');
const Web3 = require("web3");
const { App } = require("@slack/bolt");
const { logger } = require('./utils')
const { formatMessage } = require('./formatting')

// Provides bot with required info needed to authenticate
// with slack
const bot = new App({
    token: process.env.SLACK_BOT_TOKEN,
    signingSecret: process.env.SLACK_SIGNING_SECRET,
  });

// Starts bot server
(async () => {
    const port = 3001
    await bot.start(process.env.PORT || port);
    logger.info(`⚡️ Slack Bolt bot is running on port ${port}!`);
})();

// Triggered when a user enters `@<bot_name> test`
// in slack
bot.message("test", async ({ command, say }) => {
  try {
    say("Hello! The bot is working!");
  } catch (error) {
    logger.error("err")
    logger.error(JSON.stringify(error));
  }
});

// Establish connection to Matic/Polygon blockchain node
const web3 = new Web3(process.env.MATIC_RPC_URL_MAINNET);
// Not needed yet
// web3.eth.accounts.wallet.add(process.env.PRIVATE_KEY)

// Store the WETH address
// Note: On Matic/Polygon this address is actually the address of WMATIC
var WETHaddress;

// Handler function for PairCreated event in QuickSwap Factory contract
async function parsePairCreatedEvent(event){
    var {token0, token1, pair} = event.returnValues;
    // Flag to indicate whether or not one of the tokens
    // in the pair is WETH
    var WETHinPair = false;
    if(token0 == WETHaddress){
        token0 = "(WETH) " + token0;
        WETHinPair = true;
    }
    else if(token1 == WETHaddress){
        token1 = "(WETH) " + token1;
        WETHinPair = true;
    }

    // Format the pair data for logging and slack
    const pairDataMessage = formatMessage(token0, token1, pair, event.transactionHash)
    logger.info(pairDataMessage)

    // Attempt to send the pair data to the slack random channel
    // if WETH in the pair
    if(WETHaddress){
      try {
        const result = await bot.client.chat.postMessage({
          channel: 'random',
          text: `${pairDataMessage}`
        });
        logger.debug(JSON.stringify(result));
      }
      catch (error) {
        logger.error(JSON.stringify(error));
      }
    }
}

// Logic for facilitate listening to new PairCreated events in QuickSwap
(async () => {
    // Initialize a pointer to the QuickSwapFactory and QuickswapRouter contracts
    // Note: these contracts are forked from Uniswap and have the same exact interface
    const QuickSwapFactory = new web3.eth.Contract(abis.UniswapV2Factory, addresses.matic.QuickSwapFactory)
    const QuickSwapRouter = new web3.eth.Contract(abis.UniswapV2Router02, addresses.matic.QuickSwapRouter)

    WETHaddress = await QuickSwapRouter.methods.WETH().call()

    // Get all PairCreated events starting from the 1000 blocks preceeding the current blockchain block
    var blockNumber = await web3.eth.getBlockNumber();
    QuickSwapFactory.events.PairCreated({fromBlock: blockNumber - 1000},function(error, event){})
        .on("connected", function(subscriptionId){
            logger.info(`Subscription ID: ${subscriptionId}`);
        })
        .on('data', function(event){
            parsePairCreatedEvent(event);
        })
        .on('error', function(error, receipt) {
            // If the transaction was rejected by the network with a receipt, the second parameter will be the receipt.
            logger.error(`Error: ${JSON.stringify(error)}`)
        });
})();


