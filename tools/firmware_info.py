#!/usr/bin/env python3

# Format of Tonibox OFW Image:
#
# from -160 to -153 the git shorthash
# from -152 to -140 the creation date
# from -64 to EOF the SHA256 hash of the file
#

import hashlib
import re
import sys
import argparse
import os
import fnmatch
import json

# some global variables
# Images types
TYPE_BOOTINFO = 0
TYPE_BL = 1
TYPE_FW = 2
#IMG_TYPE = 0
# boot modes
MODE_NOTEST = 0
MODE_TESTREADY = 1
MODE_TESTING = 2
BOOT_MODE = 0

BOOT_MODES = ["NOTEST", "TESTREADY", "TEST" ]

# 0xBEAC0005 seems to identify the file end in the mcuimgX.bin files
search_pattern = bytes([0x05, 0x00, 0xac, 0xbe])
#search_pattern_bl = bytes([0x05, 0x00, 0xac, 0xbe])

def identifyFileType(data, inputfile):
   # first lets check if the image is of type mcubootinfo.bin
   file_size = os.stat(inputfile).st_size
   if file_size == 8:
      return TYPE_BOOTINFO
   elif data[-4:] == search_pattern:
      return TYPE_BL
   elif data[-68:-64] == search_pattern:
      return TYPE_FW
   else:
      raise Exception("FILE TYPE NOT SUPPORTED")
   return -1


def doBoloParsing(data):
   # find the git shorthash at -96 to -89
   # find the date at -88 to -59
   return [(data[-96:-89].decode('utf-8')),(data[-88:-59].decode('utf-8'))]
   

def doBootInfoParsing(data):
   result_dict = {'Slot':[],'Mode':[]}
   
   # get selected image
   slot = ord(data[0:1])
   slotText = "mcuimg"+str(slot+1)+".bin"+" (0x0"+str(slot)+")"
   result_dict['Slot'].append(slotText)

   # ARM is little endian
   IMG_STATUS_TESTING = bytes([0x21, 0x43, 0x34, 0x12])     # from flc.c 0x12344321
   IMG_STATUS_TESTREADY = bytes([0x65, 0x87, 0x78, 0x56])   # from flc.c 0x56788765
   IMG_STATUS_NOTEST = bytes([0xBA, 0xDC, 0xCD, 0xAB])      # from flc.c 0xABCDDCBA

   mode_dict = {0 : 'NOTEST', 1 : 'TESTING', 2 : 'TESTREADY'}

   match_list = [IMG_STATUS_NOTEST, IMG_STATUS_TESTING, IMG_STATUS_TESTREADY]
   result_dict['Mode'].append(mode_dict[match_list.index(data[4:8])])

   result_str = ('\n'.join("{}: {}".format(k, v) for k, v in result_dict.items())).replace("[","").replace("]","").replace("'","")
   return result_str
   

def doJSONDump(data, inputfile):
   data = {'Filename': inputfile, 'FWInfo': findFWInfo(data), 'creationDate': findCreationDate(
      data), 'git shorthash': findGITHash(data), 'sha256': findHash(data), 'calculatedHash': calcHash(data)}
   return json.dumps(data, indent=4)


def doCSVHeader():
    data = "Filename" + ";" +"Filetype" + ";" + "Version1" + ";" + "Version2" + ";" + \
        "Creation Date" + ";" + "git short hash" + \
        ";" + "hash" + ";" + "calculated hash" + ";" + "boot mode" + ";" + "selected slot"
    return data


def doCSVDump(data, inputfile):
   #if (filetype == TYPE_FW):
   fwInfo = findFWInfo(data)
   if len(fwInfo) > 0:
      version1 = fwInfo[0]
   else:
      version1 = ""
   if len(fwInfo) > 1:
      version2 = fwInfo[1]
   else:
      version2 = ""
   data = inputfile  +";" + version1 + ";" + version2 + ";" + findCreationDate(
      data) + ";" + findGITHash(data) + ";" + findHash(data) + ";" + calcHash(data)
   #elif (type == TYPE_BOOTINFO):
   #   bootinfo = doBootInfoParsing(data)
    #  data = inputfile + ";" + type + ";" + "" + ";" + "" + ";" + "" + ";" + "" + ";" + "" + ";" + "" + ";" + bootinfo['Mode'] + ";" + bootinfo['Slot']
   return data


def printAllInfo(data):
    versions = findFWInfo(data)
    for i in versions:
        print("Firmware Version: \t"+i)
    print("\nCreation Date: \t\t" + findCreationDate(data))
    print("\nRead SHA256: \t\t" + findHash(data))
    print("Calculated SHA256: \t" + calcHash(data))
    print("GIT Shorthash: \t\t" + findGITHash(data))
    return


def findFWInfo(data):
    # find version number with regular expression
    # search for matches of the byte patter 0500acbe
    # use that byte pattern as an anchor for our search
    # assuming the string won't get to big we are jumping backwards
    # and search
    versions = []
    for iter in re.finditer(b'\x05\x00\xac\xbe', data):
        search = data[iter.start()-100: iter.start()]
        for x in re.finditer(rb'(EU_V|PD_V|US_V|UK_V).{3}(\.[0-9]).*', search):
            versions = x.group().decode("utf-8").split('\x00')
    return list(filter(None, versions))


def findCreationDate(data):
    # get the creation date
    return data[-152:-140].decode('utf-8')


def findHash(data):
    # print out the SHA256 hash given in the binary file
    # the hash is located directly at the end of the file
    sha256 = data[-64:].decode('utf-8')
    return sha256


def calcHash(data):
    # lets do a hash calculation of the raw file data by our own for comparing
    calcedhash = hashlib.sha256(data[:-64]).hexdigest()
    return calcedhash


def findGITHash(data):
   # jump to offset -160 relativ to end of file, here we are asuming and git
   # shorthash can be found it is 7 digits per default so it ends
   # at -153 relativ to the end
   return data[-160:-153].decode('utf-8')
   

def main(argv):

   parser = argparse.ArgumentParser()
   parser.add_argument("FILE", help="input file")
   group = parser.add_mutually_exclusive_group()
   dumpgroup = parser.add_mutually_exclusive_group()
   group.add_argument("-H", "--sha256", action="count",
                     help="find sha256 hash stored in file", default=0)
   group.add_argument("-c", "--calcHash", action="count",
                     help="calculate sha256 hash of file content", default=0)
   group.add_argument("-a", "--all", action="count",
                     help="output everything (default)", default=0)
   group.add_argument("-g", "--git", action="count",
                     help="output git hash from file", default=0)
   group.add_argument("-d", "--date", action="count",
                     help="output creation date", default=0)
   group.add_argument("-V", "--version", action="count",
                     help="output version strings from file", default=0)
   group.add_argument("-r", "--recursive", action="count",
                     help="recursive extracting (in recursive mode option -all is used)", default=0)
   dumpgroup.add_argument("-j", "--json", action="count",
                        help="dump output in json format", default=0)
   dumpgroup.add_argument("-C", "--csv", action="count",
                        help="dump output in csv format", default=0)

   args = parser.parse_args()

   inputfile = args.FILE
   if not(args.recursive):
      with open(inputfile, "rb") as binary_file:
         # Read the whole file at once
         data = binary_file.read()
         # Return the hexadecimal representation of the binary data, byte instance
         type = identifyFileType(data, inputfile)

   try:
      if not(args.recursive) and type == TYPE_BOOTINFO:
         print (doBootInfoParsing(data))
      elif not(args.recursive) and type == TYPE_BL:
         print (doBoloParsing(data))
      elif args.sha256:
         print(findHash(data))
      elif args.calcHash:
         print(calcHash(data))
      elif args.git:
         print(findGITHash(data))
      elif args.date:
         print(findCreationDate(data))
      elif args.version:
         print(findFWInfo(data))
      elif args.recursive:
         json_list = []
         if (args.csv):
               print(doCSVHeader())
         for root, dirnames, filenames in os.walk(inputfile):
               for filename in fnmatch.filter(filenames, '*.bin'):
                  with open(os.path.join(root, filename), "rb") as binary_file:
                     try: 
                        # Read the whole file at once
                        data = binary_file.read()
                        type = identifyFileType(data, os.path.join(root, filename))
                        if (args.json):
                           if (type == TYPE_BOOTINFO):
                              print ('Found bootinfo file skipped for JSON-Output: ')
                              print( doBootInfoParsing(data) )
                           elif (type == TYPE_BL):
                              print ('Found bootloader file skipped for JSON-Output: ')
                              print (*doBoloParsing(data), sep = "\n")
                           else:
                              json_list.append(json.loads(doJSONDump(
                                 data, os.path.join(root, filename))))
                        elif (args.csv):
                           if (type == TYPE_FW):
                              print(doCSVDump(data, os.path.join(root, filename)))
                        else:
                              print('\n\nFilename: '+ os.path.join(root, filename))
                              if (type == TYPE_BOOTINFO):
                                 print( doBootInfoParsing(data) )
                                 #print( ('\n'.join("{}: {}".format(k, v) for k, v in doBootInfoParsing(data).items())).replace("[","").replace("]","").replace("'","") )
                              elif (type == TYPE_BL):
                                 print (*doBoloParsing(data), sep = "\n")
                              else:
                                 printAllInfo(data)
                     except:
                        print("File not supported: " + os.path.join(root, filename))
         if (args.json):
            print(json.dumps(json_list, indent=4))
      elif args.json:
         print(doJSONDump(data, inputfile))
      else:
         printAllInfo(data)
   except:
         print("File not supported: "+ inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
