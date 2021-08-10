#!/usr/bin/env python
from twisted.internet import reactor, protocol, task
from HTTPClient import HTTPClientFactory, HTTPClientOpts
import sys
import logging
from optparse import OptionParser

# create logger
logging.basicConfig()
logger = logging.getLogger('client')

parser = OptionParser()
parser.add_option("-d", "--dest", dest="destIp", help="server ip")
parser.add_option("--host", dest="host", help="hostname")
parser.add_option("-c", "--close", dest="closeDelay", help="close delay", default=1)
parser.add_option("-t", "--think", dest="think", help="think time", default=0.1)
parser.add_option("-b", "--bytes", dest="totalBytes", help="total bytes to request", default=500000)
parser.add_option("--min", dest="contentLenMin", help="min content length per request (K)", default=1)
parser.add_option("--max", dest="contentLenMax", help="max content length per request (K)", default=1)
parser.add_option("--ua", dest="userAgent", help="User agent string", default=None)
parser.add_option("-i", "--interface", dest="interface", help="interface", default=None) 
parser.add_option("-p", dest="port", help="port", default=80)
parser.add_option("--loglevel", dest="logLevel", help="Log level of output messages, possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG", default="WARNING")

def main():
    (options, args) = parser.parse_args()
    # Set logging level
    logLevel = logging.getLevelName(options.logLevel)
    logger.setLevel(logLevel)

    clientOpts = HTTPClientOpts(options.host,
                                thinkTime = float(options.think),
                                totalBytes = int(options.totalBytes),
                                contentLengthMin = int(options.contentLenMin),
                                contentLengthMax = int(options.contentLenMax),
                                closeDelay = int(options.closeDelay),
                                userAgent = options.userAgent)

    f = HTTPClientFactory(options.destIp, int(options.port), clientOpts, timeout = 5, bindAddress=options.interface)

    reactor.callWhenRunning(f.start)

    l = task.LoopingCall(f.logStats)
    l.start(5)
    ll = task.LoopingCall(f.logStatsRANEfficiency)
    ll.start(5)

    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
