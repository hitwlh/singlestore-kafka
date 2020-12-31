#!/usr/bin/python

import struct
import sys

binary_stdin = sys.stdin if sys.version_info < (3, 0) else sys.stdin.buffer
binary_stderr = sys.stderr if sys.version_info < (3, 0) else sys.stderr.buffer
binary_stdout = sys.stdout if sys.version_info < (3, 0) else sys.stdout.buffer

def input_stream():
    """
        Consume STDIN and yield each record that is received from SingleStore DB
    """
    while True:
        byte_len = binary_stdin.read(8)
        if len(byte_len) == 8:
            byte_len = struct.unpack("L", byte_len)[0]
            result = binary_stdin.read(byte_len)
            yield result
        else:
            assert len(byte_len) == 0, byte_len
            return


def log(message):
    """
        Log an informational message to stderr which will show up in SingleStore DB in
        the event of transform failure.
    """
    binary_stderr.write(message + b"\n")


def emit(message):
    """
        Emit a record back to SingleStore DB by writing it to STDOUT.  The record
        should be formatted as JSON, Avro, or CSV as it will be parsed by
        LOAD DATA.
    """
    binary_stdout.write(message + b"\n")

log(b"Begin transform")

# We start the transform here by reading from the input_stream() iterator.
for data in input_stream():
    # Since this is an identity transform we just emit what we receive.
    emit(data)

log(b"End transform")
