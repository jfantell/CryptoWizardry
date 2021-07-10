const UniswapV2Router02 = require('./UniswapV2Router02.json')
const UniswapV2Factory = require('././UniswapV2Factory.json')
const UniswapV2Pair = require('./UniswapV2Pair.json')
const ERC20 = require('./ERC20.json')

module.exports = {
    abis : {
        UniswapV2Router02,
        ERC20,
        UniswapV2Factory,
        UniswapV2Pair
    }
}