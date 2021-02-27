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

def doJSONDump(data, inputfile):
   data = {'Filename': inputfile, 'FWInfo': findFWInfo(data), 'creationDate': findCreationDate(data), 'git shorthash': findGITHash(data), 'sha256': findHash(data), 'calculatedHash': calcHash(data)}
   return json.dumps(data, indent=4)

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

   args = parser.parse_args()

   inputfile = args.FILE
   if not(args.recursive):
      with open(inputfile, "rb") as binary_file:
         #Read the whole file at once
         data = binary_file.read()
         #Return the hexadecimal representation of the binary data, byte instance

   if args.sha256:
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
         for root, dirnames, filenames in os.walk(inputfile):
            for filename in fnmatch.filter(filenames, '*.bin'):
               #print("--\nfilename: ", os.path.join(root, filename))
               #matches.append(os.path.join(root, filename))
               #doJSONDump(data, os.path.join(root, filename))
               with open(os.path.join(root, filename), "rb") as binary_file:
                  #Read the whole file at once
                  data = binary_file.read()
                  if (args.json):
                     json_list.append(json.loads(doJSONDump(data, os.path.join(root, filename))))

                     #jsonMerge = {**json.loads(jsonMerge), **json.loads(doJSONDump(data, os.path.join(root, filename)))}
                     #temp = foo['Files'] 
                     #temp.append(foo)
                     #print(json.dumps(jsonMerge, indent=4))
                  else:
                     printAllInfo(data)
               if (args.json):
                  print(json.dumps(json_list, indent=4))
         #print(matches)
   elif args.json:
      print(doJSONDump(data, inputfile) )     
   else:
      printAllInfo(data)


if __name__ == "__main__":
   main(sys.argv[1:])
