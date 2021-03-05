#!/usr/bin/env python3

import argparse
import binascii
import os
import sys
from dataclasses import dataclass
from datetime import date
from asn1crypto.x509 import Certificate

@dataclass
class MagicByteInfo:
    magic: bytes = None
    clientCertDate: date = None
    error: str = None
    path: str = None

    def __str__(self):
        if self.error == None:
            return self.path + "\r\n" + " Magic: 0x" + binascii.hexlify(self.magic).decode('ascii') + "\r\n" + " Not Valid Until: " + self.clientCertDate.strftime('%Y-%m-%d') + "\r\n"
        else:
            return self.path + "\r\n" + " Error: " + self.error + "\r\n"

def getMagic(data):
    # Get the magic bytes from the image
    magic = data[-8:-4]
    return magic

def search(dir):
    magic = MagicByteInfo()

    PATH_CLIENT_DER = os.path.join(dir, "cert/client.der")
    PATH_MCUIMG_BIN = os.path.join(dir, "sys/mcuimg.bin")
    SIZE_MCUIMG_BIN = 20956

    with open(PATH_CLIENT_DER, "rb") as clientDer:
        data = clientDer.read()
        cert = Certificate.load(data)
        magic.clientCertDate = cert["tbs_certificate"]["validity"]["not_before"].native.date()

    mcuimgSize = os.stat(PATH_MCUIMG_BIN).st_size
    if mcuimgSize == SIZE_MCUIMG_BIN:
        with open(PATH_MCUIMG_BIN, "rb") as mcuimgBin:
            data = mcuimgBin.read()
            magic.magic = getMagic(data)[::-1]
    else:
        raise ValueError("mcuimg.bin has the wrong filesize - " + PATH_MCUIMG_BIN)

    magic.path = dir
    return magic

def searchRecursive(dir):
    result_list = []
    for entry in os.scandir(dir):
        try:
            if entry.is_dir():
                result_list.append(search(entry.path))
        except (ValueError, FileNotFoundError) as err:
            result_list.append(MagicByteInfo(error=str(err), path=entry.path))
        

    return result_list




def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("DIR", help="Base search directoy")
    group = parser.add_mutually_exclusive_group()
    dumpgroup = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--recursive", action="count", help="recursive search in subdirs", default=0)
    dumpgroup.add_argument("-C", "--csv", action="count", help="dump output in csv format", default=0)
    args = parser.parse_args()

    result_list = []

    if not(args.recursive):
        result = search(args.DIR)
        result_list.append(result)
    else:
        result_list = searchRecursive(args.DIR)

    if (args.csv):
        print("Cert not valid until;Magic Bytes;Path")
    for result in result_list:
        if (args.csv):
            if result.error == None:
                print(result.clientCertDate.strftime('%Y-%m-%d') + ";" + "0x" + binascii.hexlify(result.magic).decode('ascii') + ";" + result.path)
        else:
            print(result)

if __name__ == "__main__":
    main(sys.argv[1:])
