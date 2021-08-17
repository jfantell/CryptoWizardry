const { createLogger, format, transports } = require('winston');

const getDateTime = () => {
    return new Date().toISOString().
    replace(/T/, ' ').      // replace T with a space
    replace(/\..+/, '')     // delete the dot and everything after
}

const logger = createLogger({
  level: 'debug',
  timestamp: true,
  format: format.printf(info => `${getDateTime()} [${info.level.toUpperCase()}] ${info.message}`),
  transports: [
    //
    // - Write to all logs with level `info` and below to `combined.log` 
    // - Write all logs error (and below) to `error.log`
    //
    new transports.File({ filename: './logs/error.log', level: 'error', options: { flags: 'w' }}),
    new transports.File({ filename: './logs/combined.log', options: { flags: 'w' }})
  ]
});

module.exports = {
    logger,
    getDateTime
}