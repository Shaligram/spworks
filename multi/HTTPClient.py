
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol, task
from twisted.protocols.policies import TimeoutMixin
import sys
import time
import struct
import random
import logging
import pdb

# create logger
logging.basicConfig()
logger = logging.getLogger('client')

class HTTPClientOpts:
    def __init__(self, host, thinkTime = 0.1, totalBytes = 500000, contentLengthMin = 3, contentLengthMax = 10, closeDelay = 1, latency = 0.5, userAgent = "HTTPClient"):
        self.host = host
        self.thinkTime = thinkTime
        self.totalBytes = totalBytes
        self.contentLengthMin = contentLengthMin
        self.contentLengthMax = contentLengthMax
        self.closeDelay = closeDelay
        self.latency = latency
        self.userAgent = userAgent

class HTTPRequest:
    def __init__(self, opts, contentLen):
        self.opts = opts
        self.contentLen = contentLen
    
    def writeTo(self, transport):
        transport.write('GET /%d HTTP/1.1\r\n' % (self.contentLen))
        transport.write('User-Agent: %s\r\n' % (self.opts.userAgent))
        transport.write('Host: %s\r\n' %(self.opts.host))
        transport.write('Accept: */*\r\n')
        transport.write('\r\n')
        
class HTTPResponse:
    def __init__(self, requestedLen):
        self.requestedLen = requestedLen
        self.response = ''
        self.headerLen = 0
        self.bodyLen = 0
        self.totalLen = 0
        self.readTimeout = 0
    def read(self, data):
        dataLen = len(data)
        self.totalLen += len(data)
        logger.debug("Received %d %d %d" % ( dataLen, self.totalLen, self.requestedLen))
        if self.headerLen == 0:
            logger.info("Checking for headers")
            self.response = self.response.join(data)
            endOfHeaders = self.response.find('\r\n\r\n')
            logger.debug("Checking for headers %d" % (endOfHeaders))
            if endOfHeaders > 0:
                logger.debug("Headers found at %d" % (endOfHeaders))
                self.headerLen = endOfHeaders
		headersContent = self.response[:self.headerLen]
                requestLine, headersAlone = headersContent.split('\r\n', 1)
                logger.debug("HTTP response %s" % (requestLine))
                if not requestLine.find('OK') > 0:
                    logger.warn("HTTP error responsed: %s" % (requestLine))
		if headersAlone.find('KeepAlive-Timeout:') >= 0:
                   headersAlone = headersAlone.split('\r\n')
                   for curr in headersAlone:
                       if curr.find('KeepAlive-Timeout:') >= 0:
                           name, value = curr.split(":", 1)
                           if value.endswith("\r\n"):
                               value = value[:-2]
                           value = value.lstrip()
                           self.readTimeout = int(value)
                           logger.debug("Read: Find KeepAlive-Timeout: %d" % (self.readTimeout))
            self.bodyLen = self.totalLen - self.headerLen - 4
        else:
            self.bodyLen += dataLen
    def isComplete(self):
        return  self.bodyLen == self.requestedLen

class HTTPClient(protocol.Protocol, TimeoutMixin):
    SendingRequest = 1
    ReadingResponse = 2
    def __init__(self, opts):
        self.opts = opts

    def connectionMade(self):
        logger.info("connectionMade")
        self.setTimeout(None) # No read timeout
        self.received = 0
        self.contentLen = 0
        self.state = HTTPClient.SendingRequest
        self.shLen = 0
        self.tmpData = None
        self.startTime = time.time() 
        self.makeRequest()

    def connectionLost(self, reason):
	self.spentTime = time.time() - self.startTime
        logger.debug("connectionLost: The connection was closed after %.2f second(s)" % (self.spentTime))
        logger.debug("connectionLost: Keep Alive timeoute on server - %d" % (self.response.readTimeout))
        # Don't check spent time if conection is closed in a non-clean fashion
        if reason.getErrorMessage() == 'Connection was closed cleanly.': 	
            if (self.response.readTimeout > 0) and (self.spentTime > (self.response.readTimeout + self.opts.latency)):
               logger.info("Seems like FIN has been buffered for %.2f second(s)" % (self.spentTime - self.response.readTimeout))
               self.transport.connector.factory.totalBuffered += 1 
    
    def makeRequest(self):
        int(random.triangular(self.opts.contentLengthMin, self.opts.contentLengthMax) * 1024)
        while(self.contentLen < 1024):
            self.contentLen = int(random.triangular(self.opts.contentLengthMin, self.opts.contentLengthMax) * 1024)

        logger.debug("Requesting %d bytes", self.contentLen)
        request = HTTPRequest(self.opts, self.contentLen)
        request.writeTo(self.transport)
        self.response = HTTPResponse(self.contentLen)
        self.state = HTTPClient.ReadingResponse

    def closeConnection(self):
        self.transport.loseConnection()

    def dataReceived(self, data):
        if self.state == HTTPClient.ReadingResponse:
            self.response.read(data)
            if self.response.isComplete():
                logger.debug("Received expected len %d" % (self.contentLen))
		receivedTime = time.time() - self.startTime
		logger.info("T %.4f" % (receivedTime))
                self.received += self.contentLen
                if(self.received >= self.opts.totalBytes):
                    logger.debug("Received %d, closing", self.received)
                    if self.opts.closeDelay > 0:
                        reactor.callLater(self.opts.closeDelay, self.closeConnection)
                    else:
                        self.closeConnection()
                else:
                    logger.info("Making another request in %d", self.opts.thinkTime)
                    self.state = HTTPClient.SendingRequest
                    reactor.callLater(self.opts.thinkTime, self.makeRequest)
    
class HTTPClientFactory(protocol.ClientFactory):
    protocol = HTTPClient

    def __init__(self, host, port, opts, timeout = 30, bindAddress = None):
        self.host = host
        self.ipStart = None
        self.clientIpStart = None
        if ':' in self.host:
            (ipStart, ipEnd) = self.host.split(':')
            self.ipStart = map(int, ipStart.split('.'))
            self.ipEnd = map(int, ipEnd.split('.'))
        self.port = port
        self.totalConnections = 0
        self.lastTotalConnections = 0
        self.activeConnections = 0
        self.lastBuffered = self.totalBuffered = 0
        self.timeout = timeout
        self.bindAddress = bindAddress
        self.opts = opts
        if self.bindAddress and ':' in self.bindAddress:
            (ipStart, ipEnd) = self.bindAddress.split(':')
	    logger.info("splitting bind address")
            self.clientIpStart = map(int, ipStart.split('.'))
            self.clientIpEnd = map(int, ipEnd.split('.'))

    def buildProtocol(self, addr):
        return HTTPClient(self.opts)

    def newClient(self):
        self.totalConnections += 1
        self.activeConnections += 1
        destIp = self.host
        if self.ipStart:
            destIp = "%d.%d.%d.%d" % (random.randint(self.ipStart[0], self.ipEnd[0]),
                                      random.randint(self.ipStart[1], self.ipEnd[1]),
                                      random.randint(self.ipStart[2], self.ipEnd[2]),
                                      random.randint(self.ipStart[3], self.ipEnd[3]))
        bindAddress = self.bindAddress
        if self.clientIpStart:
            bindAddress = "%d.%d.%d.%d" % (random.randint(self.clientIpStart[0], self.clientIpEnd[0]),
                                      random.randint(self.clientIpStart[1], self.clientIpEnd[1]),
                                      random.randint(self.clientIpStart[2], self.clientIpEnd[2]),
                                      random.randint(self.clientIpStart[3], self.clientIpEnd[3]))
   
        reactor.connectTCP(destIp, self.port, self, self.timeout, (bindAddress, 0) if bindAddress else None )

    def clientConnectionFailed(self, connector, reason):
        logger.warn("Connection failed - goodbye! %s" % (reason))
    
    def clientConnectionLost(self, connector, reason):
        logger.info("Connection lost - %s" % (reason))
        self.activeConnections -= 1

    def start(self):
        self.newClient()

    def logStats(self):
        print("Current connections : total %d (%d)   active %d" % (self.totalConnections, self.totalConnections-self.lastTotalConnections, self.activeConnections))
        self.lastTotalConnections = self.totalConnections

    def logStatsRANEfficiency(self):
        print("Buffered : total - %d, last period - %d" % (self.totalBuffered, self.totalBuffered - self.lastBuffered))
        self.lastBuffered = self.totalBuffered
