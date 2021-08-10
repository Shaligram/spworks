#!/usr/bin/env python 
from os import fork 
from twisted.internet import reactor, protocol
from HTTPServer import HTTPFactory, HTTP, HTTPServerOpts
import logging
from optparse import OptionParser

# create logger
logging.basicConfig()
logger = logging.getLogger('server')

parser = OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="interface to listen on", default="0.0.0.0")
parser.add_option("-n", "--num", dest="num", help="number of servers to start", default=1)
parser.add_option("-t", "--timeout", dest="timeout", help="read timeout, 0 = no timeout", default = 0)
parser.add_option("-p", "--port", dest="port", help="port", default = 80)
parser.add_option("--loglevel", dest="logLevel", help="Log level of output messages, possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG", default="WARNING")

def main():
    (options, args) = parser.parse_args()
    # Set logging level
    logLevel = logging.getLevelName(options.logLevel)
    logger.setLevel(logLevel)

    serverOpts = HTTPServerOpts(readTimeout = int(options.timeout))

    factory = HTTPFactory(serverOpts)
    factory.protocol = HTTP

    reactor.listenTCP(interface=options.interface, port=int(options.port), factory=factory, backlog=20480)

    for i in range(int(options.num)-1):
        print "Forking %d" % (i)
        if fork() == 0:
            # Proceed immediately onward in the children.
            # The parent will continue the for loop.
            break

    reactor.run()


if __name__ == '__main__':
    main()
