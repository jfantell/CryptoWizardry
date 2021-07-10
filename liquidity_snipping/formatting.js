const { getDateTime } = require('./utils')

function formatMessage(token0, token1, pair, transactionHash){
    var message = ""
    message += "\n============================\n";
    message += `Transaction Hash: ${transactionHash}\n`;
    message += `Timestamp: ${getDateTime()}\n`
    message += `Token 1 Address: ${token0}\n`;
    message += `Token 2 Address: ${token1}\n`;
    message += `Pair Address: ${pair}\n`;
    message += "============================\n";
    return message
}

module.exports = {
    formatMessage
}