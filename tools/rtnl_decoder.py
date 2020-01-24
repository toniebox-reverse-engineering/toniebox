#!/usr/bin/env python3

from dataclasses import dataclass
import logging

import argparse
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

FILE_MAGIC = bytearray([0x0D, 0x0A])
BLOCK_MAGIC_START = bytearray([0x18, 0x01, 0x20])
BLOCK_MAGIC_START_SKIP = bytearray([0x18, 0x04, 0x20])
BLOCK_MAGIC_START_SKIP2 = bytearray([0x18, 0x03, 0x20])
BLOCK_MAGIC_END = bytearray([0x45 ,0x38 ,0x1D ,0xE9 ,0x5D])

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)

p = parser.parse_args()
print(p.file_path, type(p.file_path), p.file_path.exists())

log_file = p.file_path
logging.info("Decoding Toniebox bytestream...")

logging.info("Opening file %s", log_file)

with open(log_file, mode='rb') as file:
    data = file.read()

if not data.startswith(FILE_MAGIC):
    logging.error("Magic bytes not found...")
    exit(1)

cursor = len(FILE_MAGIC)

@dataclass
class Data_Block:
    start: int
    end: int
    data: bytearray
    unknown_1: bytearray
    protobuf_type: int
    protobuf_length: int
    data_block: bytearray
    unknown_2: bytearray

    def __hexify(self, byteblock):
        return " ".join(["{:02x}".format(x) for x in byteblock])

    def __as_hex(self, integer):
        return "0x%0.2x" % integer

    def __repr__(self):
        return "Data Block\n\tstart: %s\n\tend: %s\n\tunknown_1: %s\n\tprotobuf_type: %s\n\tprotobuf_length: %s\n\tblock: %s\n\tunknown_2: %s\n\tdata: %s\n\ttext: %s" \
        % (self.__as_hex(self.start), self.__as_hex(self.end), self.__hexify(self.unknown_1), self.__as_hex(self.protobuf_type), self.protobuf_length, self.__hexify(self.data_block), self.__hexify(self.unknown_2), self.__hexify(self.data), self.data_block)

while not data[cursor:].startswith(BLOCK_MAGIC_START):
    cursor += 1
    if cursor == len(data)-1:
        logging.error("No magic start found")
        exit(1)

while data[cursor:].startswith(BLOCK_MAGIC_START):
    start = cursor
    cursor += len(BLOCK_MAGIC_START)

    if data[cursor+2] == 0x3C or data[cursor+2] == 0x50:
        unknown_1 = data[cursor:cursor+3]
        cursor += 3
    else:
        unknown_1 = data[cursor:cursor+4]
        cursor += 4

    protobuf_type = data[cursor]
    cursor += 1
    if protobuf_type == 0x20:
        protobuf_len = 32
    else:
        protobuf_len = data[cursor]
        cursor += 1

    data_block = data[cursor:cursor+protobuf_len]
    cursor += protobuf_len
    if not data[cursor:].startswith(BLOCK_MAGIC_END):
        logging.error("Magic block end not found")
        data_block = Data_Block(start, 0, data[start:], unknown_1, protobuf_type, protobuf_len, data_block, bytearray([]))
        print(data_block)
        break
    cursor += len(BLOCK_MAGIC_END)
    unknown_2 = data[cursor:cursor+17]
    cursor += 17

    if unknown_1[0] == 0x01: # and protobuf_len == 0:
        cursor +=13
    elif unknown_1[0] == 0x08:
        cursor += 9

    end = cursor
    data_block = Data_Block(start, end, data[start:end], unknown_1, protobuf_type, protobuf_len, data_block, unknown_2)
    print(data_block)

    while data[cursor:].startswith(BLOCK_MAGIC_START_SKIP): #skip block tbd
        data_block = Data_Block(cursor, cursor+34, data[cursor:cursor+34], bytearray([]), 0, 0, bytearray([]), bytearray([]))
        print(data_block)
        cursor += 34
    while data[cursor:].startswith(BLOCK_MAGIC_START_SKIP2): #skip block tbd
        data_block = Data_Block(cursor, cursor+38, data[cursor:cursor+38], bytearray([]), 0, 0, bytearray([]), bytearray([]))
        print(data_block)
        cursor += 38

if cursor < len(data)-1:
    logging.error("Cursor not at the end (%i!=%i)" % (cursor, len(data)-1))
    print(data[cursor:])
logging.info("Done")