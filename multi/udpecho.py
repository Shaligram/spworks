import socket
import IN
import sys
import time
import timeit

i = 1
while i < 2:
    i += 1

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((sys.argv[1], 0))

    server_address = (sys.argv[2], int(sys.argv[3]))
    message = 'x' * 1000

    try:

        # Send data
        #print >>sys.stderr, 'sending "%s"' % message
        sendTime = time.time()
        sent = sock.sendto(message, server_address)

        # Receive response
        data, server = sock.recvfrom(4096)
        recvTime = time.time()
        #print >>sys.stderr, 'received "%d"' % len(data)

        time.sleep(2)

        send2Time = time.time()
        sent = sock.sendto(message, server_address)
        data, server = sock.recvfrom(4096)
        recv2Time = time.time()

        send3Time = time.time()
        sent = sock.sendto(message, server_address)
        data, server = sock.recvfrom(4096)
        recv3Time = time.time()

        send4Time = time.time()
        sent = sock.sendto(message, server_address)
        data, server = sock.recvfrom(4096)
        recv4Time = time.time()

        print >> sys.stderr, "T %.4f %.4f %.4f %.4f" %(recvTime-sendTime, recv2Time-send2Time, recv3Time-send3Time, recv4Time-send4Time)
    finally:
        #print >>sys.stderr, 'closing socket'
        sock.close()


