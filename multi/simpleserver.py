#!/usr/bin/env python 
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol
import sys
from HTTPServer import HTTPFactory, HTTP, HTTPServerOpts
import struct
import logging
from optparse import OptionParser

# create logger
logging.basicConfig()
logger = logging.getLogger('server')

parser = OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="interface to listen on", default="0.0.0.0")
parser.add_option("-t", "--timeout", dest="timeout", help="read timeout", default = 0)
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
    reactor.listenTCP(interface=options.interface, port = int(options.port), factory=factory, backlog=2048)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
