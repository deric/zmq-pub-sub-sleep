#!/usr/bin/env python

import logging
import os
import sys
import argparse
import math
import zmq
import time
from contextlib import contextmanager


def run(host_address, delay):
    logging.info("Current libzmq version is %s" % zmq.zmq_version())
    logging.info("Current pyzmq version is %s" % zmq.pyzmq_version())

    logging.info("Pushing messages to: %s" % host_address)
    ctx = zmq.Context.instance()

    server = ctx.socket(zmq.PUB)
    server.bind(host_address)

    i = 0
    while(True):
        delay = delay + math.exp(i)
        msg = str("msg #%i, now sleeping for %i s" % (i,delay))
        server.send_string(msg)
        logging.debug(msg)
        time.sleep(delay) # sleep
        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send slurps to Slurp-Blarg server.')
    parser.add_argument('--host', dest='host', help='Host to connect to (tcp://127.0.0.1:6500 by default)', default="tcp://*:6500")
    parser.add_argument('-v', dest='verbose', help='Verbose mode', action="store_const", const=True)
    parser.add_argument('--delay', dest='delay', type=int, help='How long to wait between messages (seconds)', default=1)
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")
    run(args.host, args.delay)
