from twisted.internet import reactor, protocol
from twisted.protocols.policies import TimeoutMixin
import sys
import logging
import struct
import re

logger = logging.getLogger('server')

class HTTPServerOpts:
    def __init__(self, readTimeout = 30):
        self.readTimeout = readTimeout

class HTTPFactory(protocol.Factory):
    def __init__(self, opts):
        self.opts = opts

    def buildProtocol(self, addr):
        return HTTP(self.opts)

class HTTPResponse:
    def __init__(self, size = 1024, readTimeout = 30):
        self.size = size
	self.readTimeout = readTimeout
    def writeTo(self, transport):
        transport.write('HTTP/1.1 200 OK\r\n')
        transport.write('Content-Length: %d\r\n' % (self.size))
        transport.write('Content-Type: x/y\r\n')
	if self.readTimeout > 0:
            transport.write('KeepAlive-Timeout: %d\r\n' % (self.readTimeout))
        transport.write('Cache-Control: no-cache\r\n')
        transport.write('\r\n')
        transport.write('x'*self.size)
        logger.debug("writeTo : response size %d" % (self.size))

class HTTPRequest:
    def __init__(self):
        self.complete = False
        self.requestedSize = 0
        self.tmpData = []
        self.requestRegex = re.compile('GET.*/(.*) HTTP/1.1')
    def read(self, data):
        self.tmpData += data
        logger.debug("###%s###" % self.tmpData[-4:])
        if self.tmpData[-4:] == ['\r', '\n', '\r', '\n']:
            self.complete = True 
            m = self.requestRegex.search(''.join(self.tmpData))
            if m:
                self.requestedSize = int(m.group(1))
        return
    def isComplete(self):
        return self.complete
    def getRequestedSize(self):
        return self.requestedSize
    def getResponse(self):
        return HTTPResponse()

class HTTP(protocol.Protocol, TimeoutMixin):
    Waiting = 0
    ReadingRequest = 1

    def __init__(self, opts):
        logger.info("Initialising new HTTP")
        self.opts = opts
        self.state = HTTP.Waiting

    def connectionMade(self):
        logger.debug("ConnectionMade : setting timeout to %d" % (self.opts.readTimeout))
        self.setTimeout(self.opts.readTimeout if self.opts.readTimeout > 0 else None)
 
    def dataReceived(self, data):
        logger.debug("Received %d %s" % (len(data), data))
        if(self.state == HTTP.Waiting):
            self.request = HTTPRequest()
            self.state = HTTP.ReadingRequest
            self.request.read(data)
            if self.request.isComplete():
                response = HTTPResponse(self.request.getRequestedSize(),self.opts.readTimeout)
                response.writeTo(self.transport)
                self.state = HTTP.Waiting
        elif (self.state == HTTP.ReadingRequest):
            self.request.read(data)
            if self.request.isComplete():
                response = HTTPResponse(self.request.getRequestedSize(),self.opts.readTimeout)
                response.writeTo(self.transport)
                self.state = HTTP.Waiting

