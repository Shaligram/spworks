#!/usr/bin/env python 

import time
from multiprocessing import Process
from os import fork
from twisted.internet import reactor, protocol, task
from HTTPClient import HTTPClientFactory, HTTPClient, HTTPClientOpts
import sys
import logging
from optparse import OptionParser
from subprocess import Popen, call

# create logger
logging.basicConfig()
logger = logging.getLogger('client')

parser = OptionParser()
parser.add_option("-d", "--dest", dest="destIp", help="server ip")
parser.add_option("--host", dest="host", help="server name")
parser.add_option("-n", "--num", dest="num", help="number of clients to fork", default=1)
parser.add_option("-r", "--rate", dest="rate", help="conn rate per client", default=10)
parser.add_option("-c", "--close", dest="closeDelay", help="close delay", default=1)
parser.add_option("-i", "--interface", dest="interface", help="interface", default=None)
parser.add_option("-t", "--think", dest="think", help="think time", default=0.1)
parser.add_option("-b", "--bytes", dest="totalBytes", help="total bytes to request", default=500000)
parser.add_option("--min", dest="contentLenMin", help="min content length per request (K)", default=1)
parser.add_option("--max", dest="contentLenMax", help="max content length per request (K)", default=1)
parser.add_option("--ua", dest="userAgent", help="User agent string", default=None)
parser.add_option("-p", dest="port", help="port", type="int", default=80)
parser.add_option("-l", "--latency", dest="latency", help="assumed network latency in seconds", type="float", default=0.5)
parser.add_option("--conlog", dest="connectionsLog", help="Connections log output refresh period, if 0 then the output is disabled", type="float", default=1)
parser.add_option("--ranlog", dest="ranLog", help="RAN Efficiency log output refresh period, if 0 then the output is disabled", type="float", default=0)
parser.add_option("--loglevel", dest="logLevel", help="Log level of output messages, possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG", default="WARNING")
parser.add_option("--duration", dest="duration", help="Duration to run client for", type="int", default=10)
parser.add_option("--pcap_file", dest="pcap_file", help="Capture packets", default=None)
parser.add_option("--pcap_iface", dest="pcap_iface", help="Capture packets on interface", default="any")
parser.add_option("-v", dest="verbose", action="store_true", help="Verbose", default=False)

#import yappi

#yappi.start()

def prof():
    print "### Func   ###"
    yappi.get_func_stats().print_all()
    print "### Thread ###"
    yappi.get_thread_stats().print_all()

def stop(reactor, task):
    task.stop()
    reactor.stop()

def childProc(options, clientOpts):
    print "childProc\n"
    factory = HTTPClientFactory(options.destIp,
                                int(options.port),
                                clientOpts,
                                timeout=30,
                                bindAddress=options.interface)
    factory.protocol = HTTPClient
    creator = task.LoopingCall(factory.start)

    connRate = (1.0 / (float)(options.rate))
    print "Using conn rate %f -> interval %f" % ((float)(options.rate), connRate)
    creator.start(connRate)
    if options.connectionsLog > 0:
        l = task.LoopingCall(factory.logStats)
        l.start(options.connectionsLog)
    if options.ranLog > 0:
        ll = task.LoopingCall(factory.logStatsRANEfficiency)
        ll.start(options.ranLog)

    reactor.callLater(options.duration, stop, reactor, creator)

    # Starting reactor
    print "Starting"
    reactor.run()

def startPacketCapture(options):
    return Popen(["sudo", "tcpdump", "-w", options.pcap_file, "-i", options.pcap_iface, "port", str(options.port)])

def dumpPacketCapture(options):
    return call(["tshark", "-t", "e", "-o", "tcp.relative_sequence_numbers:FALSE", "-r", options.pcap_file])

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
                                latency = float(options.latency),
                                userAgent = options.userAgent)
  
    pcapProcess = None
    if(options.pcap_file): 
        pcapProcess = startPacketCapture(options)

    #Process(target=startTshark, args=(options,))
    #tsharkProcess.start()

    time.sleep(1)

    print "Starting children\n"
    children = []
    for i in range(0,int(options.num)):
        print "Starting child %d of %d\n" % ((i+1), int(options.num))
        p = Process(target=childProc, args=(options,clientOpts))
        p.start()
        children.append(p)

    for child in children:
        print "Waiting for child %s\n" % (child)
        child.join()

    if pcapProcess:
        pcapProcess.terminate()
        if options.verbose:
            dumpPacketCapture(options) 
    
# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
    
