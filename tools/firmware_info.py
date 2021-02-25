#!/usr/bin/env python3

# Format of Tonibox OFW Image reversed with radare2 
#
# from -160 to -153 the git shorthash
# from -152 to -140 the creation date 
# from -64 to EOF the SHA256 hash of the file
#
#[0x00027ca9]> x -160
#- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
#0x00027c09  3333 6434 6633 6100 3134 204f 6374 2031  33d4f3a.14 Oct 1
#0x00027c19  373a 3332 0000 0000 0000 0000 0000 0000  7:32............
#0x00027c29  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00027c39  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00027c49  0000 0000 0001 0200 0100 010e 0000 0000  ................
#0x00027c59  0000 0000 0200 0000 0000 0000 0500 acbe  ................
#0x00027c69  6632 6565 3433 3365 3036 3330 6135 3632  f2ee433e0630a562
#0x00027c79  3433 3234 3237 3764 3736 3363 6533 6337  4324277d763ce3c7
#0x00027c89  6165 6131 3633 3061 3961 3037 6134 6239  aea1630a9a07a4b9
#0x00027c99  3831 3766 3039 3535 3066 3235 6665 3536  817f09550f25fe56
# 
# unfortunately the version string isn't so fix and differs in it's length
# see 3.0.6 for example in comparison to version 3.0.7. and 3.0.8
#
#[0x000266e4]> x -220
#- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
#0x00026608  0300 0000 4555 5f56 332e 302e 365f 4246  ....EU_V3.0.6_BF
#0x00026618  312d 3000 4555 5f56 332e 302e 365f 7374  1-0.EU_V3.0.6_st
#0x00026628  6162 6c65 5f62 7261 6e63 6800 0500 acbe  able_branch.....
#0x00026638  0000 0000 bb1b 4c5e 0000 0000 6161 3232  ......L^....aa22
#0x00026648  6236 3200 3138 2046 6562 2031 383a 3135  b62.18 Feb 18:15
#0x00026658  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00026668  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00026678  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00026688  0001 0200 0100 010d 0000 0000 0000 0000  ................
#0x00026698  0200 0000 0000 0000 0500 acbe 3131 6661  ............11fa
#0x000266a8  3362 3832 3733 6237 6530 6439 3837 3131  3b8273b7e0d98711
#0x000266b8  3566 6136 6263 3630 3031 6131 6166 3163  5fa6bc6001a1af1c
#0x000266c8  6339 3433 3562 3330 3338 3831 3132 3436  c9435b3038811246
#0x000266d8  6232 3030 3663 6565 6539 3866            b2006ceee98f
#f[0x000266e4]> 
#
#[0x00028418]> x -220
#- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
#0x0002833c  0100 0000 0002 0000 5044 5f56 332e 302e  ........PD_V3.0.
#0x0002834c  372d 3000 5044 5f56 332e 302e 375f 7374  7-0.PD_V3.0.7_st
#0x0002835c  6162 6c65 5f62 7261 6e63 6800 0500 acbe  able_branch.....
#0x0002836c  0000 0000 33a2 c75f 0000 0000 3339 6133  ....3.._....39a3
#0x0002837c  6166 3700 3032 2044 6563 2031 353a 3138  af7.02 Dec 15:18
#0x0002838c  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x0002839c  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x000283ac  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x000283bc  0001 0200 0100 010e 0000 0000 0000 0000  ................
#0x000283cc  0300 0000 0000 0000 0500 acbe 6233 3565  ............b35e
#0x000283dc  3665 3233 6238 3539 6662 3332 6565 3930  6e23b859fb32ee90
#0x000283ec  3838 6562 6231 6130 3961 6165 3363 6163  88ebb1a09aae3cac
#0x000283fc  3163 3933 3032 3365 3636 6166 6635 3336  1c93023e66aff536
#0x0002840c  6463 6561 3664 3564 3439 3862            dcea6d5d498b
#[0x00028418]> 
#
#[[0x00027ca9]> px -200
#- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
#0x00027be1  aaaa aa45 555f 5633 2e30 2e38 2d30 0033  ...EU_V3.0.8-0.3
#0x00027bf1  2e30 2e38 5f45 5500 0500 acbe 0000 0000  .0.8_EU.........
#0x00027c01  fb19 875f 0000 0000 3333 6434 6633 6100  ..._....33d4f3a.
#0x00027c11  3134 204f 6374 2031 373a 3332 0000 0000  14 Oct 17:32....
#0x00027c21  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00027c31  0000 0000 0000 0000 0000 0000 0000 0000  ................
#0x00027c41  0000 0000 0000 0000 0000 0000 0001 0200  ................
#0x00027c51  0100 010e 0000 0000 0000 0000 0200 0000  ................
#0x00027c61  0000 0000 0500 acbe 6632 6565 3433 3365  ........f2ee433e
#0x00027c71  3036 3330 6135 3632 3433 3234 3237 3764  0630a5624324277d
#0x00027c81  3736 3363 6533 6337 6165 6131 3633 3061  763ce3c7aea1630a
#0x00027c91  3961 3037 6134 6239 3831 3766 3039 3535  9a07a4b9817f0955
#0x00027ca1  3066 3235 6665 3536                      0f25fe56
#[0x00027ca9]> 
#
# But every version string seems to have the pattern _V included, lets try to build 
# an regular expression for it and every version string is followed by the bytes
# 0500 acbe so far, we could use that to find an start point for our search
import hashlib
import binascii
import re
import sys
import argparse


def findFWInfo(data):   
   # find version number with regular expression
   # search for matches of the byte patter 0500acbe
   # use that byte pattern as an anchor for our search
   # assuming the string won't get to big we are jumping backwards
   # and search
   for iter in re.finditer(b'\x05\x00\xac\xbe',data):
      search = data[iter.start()-100: iter.start()]
      for x in re.finditer(rb'(EU_V|PD_V|US_V|UK_V).{3}(\.[0-9]).*', search):
         versions = x.group().decode("utf-8").split('\x00')
         return versions

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
   group.add_argument("-H", "--sha256", action="count", help="find sha256 hash stored in file", default=0)
   group.add_argument("-c", "--calcHash", action="count", help="calculate sha256 hash of file content", default=0)
   group.add_argument("-a", "--all", action="count", help="output everything (default)", default=0)
   group.add_argument("-g", "--git", action="count", help="output git hash from file", default=0)
   group.add_argument("-d", "--date", action="count", help="output creation date", default=0)
   group.add_argument("-V", "--version", action="count", help="output version strings from file", default=0)
  
   args = parser.parse_args()

   inputfile = args.FILE
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
       versions = list(filter(None, findFWInfo(data)))
       for i in versions:
         print(i)
   else:
      versions = list(filter(None, findFWInfo(data)))
      for i in versions:
         print("Firmware Version: \t"+i)
      print("\nCreation Date: \t\t"+ findCreationDate(data))
      print("\nRead SHA256: \t\t"+ findHash(data))
      print("Calculated SHA256: \t"+ calcHash(data)) 
      print("GIT Shorthash: \t\t" + findGITHash(data))
   
if __name__ == "__main__":
   main(sys.argv[1:])