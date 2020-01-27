#!/usr/bin/env python3

from dataclasses import dataclass
import logging

import argparse
from pathlib import Path

import struct

logging.basicConfig(level=logging.DEBUG)

FILE_MAGIC = bytearray([0x0D, 0x0A])
BLOCK_MAGIC_END = bytearray([0x45 ,0x38 ,0x1D ,0xE9 ,0x5D])

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path, help="Path to raw toniebox protobuf log")
parser.add_argument("--output", dest="output_type", default="print", help="default=print, csv")

p = parser.parse_args()
logging.info(p.file_path, type(p.file_path), p.file_path.exists())

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
    data_raw: bytearray

    def __hexify(self, byteblock):
        return " ".join(["{:02x}".format(x) for x in byteblock])

    def __as_hex(self, integer):
        return "0x%0.2x" % integer

    def __repr__(self):
        return "Data Block\n\tstart: %s\n\tend: %s\n\tdata_raw: %s\n\tdecode: %s" \
        % (self.__as_hex(self.start), self.__as_hex(self.end), self.__hexify(self.data_raw), self.decode_protobuf("print"))

    def decode_protobuf(self, return_type=""):
        data = self.data_raw
        cursor = 0

        if return_type == "print":
            result = ""
        else:
            result = {}

        while cursor < len(data)-1:
            field_id = data[cursor]>>3
            field_type = data[cursor]&0b00000111
            cursor += 1

            if cursor == 1 and field_type == 2 and data[cursor] == len(data)-2: #skip encapsuling string
                cursor += 1
                continue
            
            start = cursor
            if field_type == 0:
                type_name = "Variant"
                content, cursor = self.__parse_variant(data, cursor)
            elif field_type == 1:
                type_name = "Fixed64"
                content, cursor = self.__parse_fixed64(data, cursor)
            elif field_type == 2:
                type_name = "String"
                content, cursor = self.__parse_string(data, cursor)
            elif field_type == 5:
                type_name = "Fixed32"
                content, cursor = self.__parse_fixed32(data, cursor)
            else:
                type_name = "Unknown"
                logging.error("Unknown field_type %i" % (field_type))
            end = cursor

            if return_type == "print":
                result += f"\n\t\t{field_id}({type_name}):\t{content}"
            else:
                if f"{field_id}" in result:
                    logging.warn(f"Field {field_id} declared multiple times")
                result[f"{field_id}"] = {"field_id": field_id, "field_type": field_type, "type_name": type_name, "content": content, "raw": self.__hexify(data[start:end])}

        return result
    
    def generate_csv(self):
        result = self.decode_protobuf()
        csv = ""
        for i in range(1, 10):
            if f"{i}" in result:
                csv = csv + str(result[f"{i}"]["content"]).replace("\n", "XXX").replace("\r", "XXX") + ";" + result[f"{i}"]["raw"] + ";"
            else:
                csv = csv + ";;"
        return csv

    def __set_bit(self, value, bit):
        return value | (1<<bit)
    def __clear_bit(self, value, bit):
        return value & ~(1<<bit)

    def __get_bit(self, value, bit):
        return (value & (1<<bit)) >> bit

    def __parse_variant(self, data, cursor):
        number = 0
        length = 0
        while True: 
            for i in range(7):
                if self.__get_bit(data[cursor+length], i):
                    number = number + (self.__set_bit(0, i+7*length))
            if not self.__get_bit(data[cursor+length], 7) or length == 7:
                break
            length +=1

        length +=1
        return (number, cursor+length)

    def __parse_fixed8(self, data, cursor):
        return (int(data[cursor]), cursor+1)
    def __parse_fixed16(self, data, cursor):
        return (struct.unpack('<h', data[cursor:cursor+2])[0], cursor+2)
    def __parse_fixed32(self, data, cursor):
        return (struct.unpack('<i', data[cursor:cursor+4])[0], cursor+4)
    def __parse_fixed64(self, data, cursor):
        return (struct.unpack('<q', data[cursor:cursor+8])[0], cursor+8)
    def __parse_string(self, data, cursor):
        length = data[cursor]
        cursor += 1
        return (data[cursor:cursor+length].decode("utf-8", "ignore"), cursor+length)
        
blocks = []

# First block
start = cursor
while cursor < len(data)-1:
    if data[cursor:].startswith(BLOCK_MAGIC_END):
        cursor += len(BLOCK_MAGIC_END)
        if data[cursor] == 0x00 and data[cursor+1] == 0x00 and data[cursor+2] == 0x00:
            end = cursor
            cursor += 3
            break
        else:
            logging.error("b1 no 3x 0x00 after magic %#x %#x %#x" % (data[cursor], data[cursor+1], data[cursor+2]))
    cursor += 1
blocks.append(Data_Block(start, end, data[start:end]))

while cursor < len(data)-1:
    length = data[cursor]
    cursor += 1
    start = cursor
    cursor += length
    end = cursor
    blocks.append(Data_Block(start, end, data[start:end]))
    if cursor < len(data)-1:
        if data[cursor] == 0x00 and data[cursor] == 0x00 and data[cursor] == 0x00:
            cursor += 3
        else:
            logging.error("b2 no 3x 0x00 after magic %#x %#x %#x" % (data[cursor], data[cursor+1], data[cursor+2]))
            break

if cursor < len(data)-1:
    logging.error("Cursor not at the end (%i!=%i)" % (cursor, len(data)-1))
    print(data[cursor:])
logging.info("Done")

for block in blocks:
    if p.output_type == "print":
        print(block)
    elif p.output_type == "csv":
        print(block.generate_csv())