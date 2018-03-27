#!/usr/bin/env python

import logging
import sys
import argparse
import zmq
import os

def run(host_address, reconnect):
    logging.info("Current libzmq version is %s" % zmq.zmq_version())
    logging.info("Current  pyzmq version is %s" % zmq.pyzmq_version())

    logging.info("Subscribing to messages from: %s" % host_address)
    c = 0 # Message count

    ctx = zmq.Context.instance()

    client = ctx.socket(zmq.SUB)
    if 'TCP_KEEPALIVE_IDLE' in os.environ:
        client.setsockopt(zmq.TCP_KEEPALIVE, 1)
        client.setsockopt(zmq.TCP_KEEPALIVE_INTVL, int(os.getenv('TCP_KEEPALIVE_INTVL', 50)))
        logging.info('setting TCP_KEEPALIVE_INTVL = %s', os.getenv('TCP_KEEPALIVE_INTVL', 50))
        client.setsockopt(zmq.TCP_KEEPALIVE_IDLE, int(os.getenv('TCP_KEEPALIVE_IDLE')))
        logging.info('setting TCP_KEEPALIVE_IDLE = %s', os.getenv('TCP_KEEPALIVE_IDLE'))
    if 'TCP_KEEPALIVE_CNT' in os.environ:
        client.setsockopt(zmq.TCP_KEEPALIVE_CNT, int(os.getenv('TCP_KEEPALIVE_CNT')))
        logging.info('setting TCP_KEEPALIVE_CNT = %s', os.getenv('TCP_KEEPALIVE_CNT'))

    client.connect(host_address)
    client.setsockopt_string(zmq.SUBSCRIBE, "")

    logging.info("HERE")
    while(True):
        message = client.recv()
        c += 1
        c = c % 1000
        logging.info("[%s] %s" % (c, message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Listens for blargs from Slurp-Blarg server.')
    parser.add_argument('--host', dest='host', help='Host to connect to (tcp://localhost:6500 by default)', default="tcp://localhost:6500")
    parser.add_argument('-v', dest='verbose', help='Verbose mode', action="store_const", const=True)
    parser.add_argument('-r', dest='reconnect', help="Reconnect after 250 messages", action="store_const", const=True, default=False)
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")
    run(args.host, args.reconnect)
