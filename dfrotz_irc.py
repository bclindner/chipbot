#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import operator
import pickle
import socket
import string
import sys
import random
import re
from time import sleep
import random
from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue, Empty
#from nbstreamreader import NonBlockingStreamReader as NBSR

class FrotzParser:
    def __init__(self):
        self.z = Popen(["dfrotz", "../zork/DATA/ZORK1.DAT"], stdin=PIPE, stdout=PIPE, bufsize=1)
        self.nbsr = NonBlockingStreamReader(self.z.stdout)

    def read_z(self, command='look'):
        fulloutput = ""
        while True:
            output = self.nbsr.readline(0.1)
            if not output:
                break
            if output[0] == '>':
                continue
            if output[0] == '\n':
                continue
            fulloutput += output
        return fulloutput
        
    def write_z(self, command):
        self.z.stdin.write(command + '\n')

# Taken from http://eyalarubas.com/python-subproc-nonblock.html
class NonBlockingStreamReader:

    def __init__(self, stream):
        """
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        """

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            """
            Collect lines from 'stream' and put them in 'queue'.
            """

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass

#f = FrotzParser()
#print f.read_z()
#com = raw_input() + '\n'
#f.write_z(com)
#print f.read_z()
