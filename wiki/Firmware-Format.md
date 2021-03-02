# Analysing the Toniebox firmware image format

The Toniebox uses the image structure just like in the cc3200-sdk from ti.
So from to-sdl/1.5.0/flc/flc.h see the following header:

```{C}
#ifndef FAST_BOOT
#define IMG_BOOT_INFO           "/sys/mcubootinfo.bin"
#define IMG_FACTORY_DEFAULT     "/sys/mcuimg1.bin"
#define IMG_USER_1              "/sys/mcuimg2.bin"
#define IMG_USER_2              "/sys/mcuimg3.bin"
#else
#define IMG_BOOT_INFO           "/sys/mcureserved.bin"
#define IMG_USER_1              "/sys/mcuimg.bin"
#define IMG_USER_2              "/sys/mcuflpatch.bin"
#endif
  
/******************************************************************************
   Image status
*******************************************************************************/
#define IMG_STATUS_TESTING      0x12344321
#define IMG_STATUS_TESTREADY    0x56788765
#define IMG_STATUS_NOTEST       0xABCDDCBA

/******************************************************************************
   Active Image
*******************************************************************************/
#define IMG_ACT_FACTORY         0
#define IMG_ACT_USER1           1
#define IMG_ACT_USER2           2
```
As we can see they are using 4 images. First one is the mcubootinfo.bin. Next one is the mcuimg1.bin and the next two images
are indented to be used for OTA updates while the first one is inteded to be the factory reset/default image kind of backup.

## Format of Toniebox Bootinfo reversed with radare2

Let's check the mcubootinfo.bin first, so open it with radare2.

```{shell}
% r2 mcubootinfo.bin 
 -- Run your own r2 scripts in awk using the r2awk program.
[0x00000000]> x
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00000000  02d8 0320 badc cdab ffff ffff ffff ffff  ... ............
0x00000010  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000020  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000030  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000040  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000050  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000060  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000070  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000080  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x00000090  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x000000a0  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x000000b0  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x000000c0  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x000000d0  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x000000e0  ffff ffff ffff ffff ffff ffff ffff ffff  ................
0x000000f0  ffff ffff ffff ffff ffff ffff ffff ffff  ................
[0x00000000]> 
```

As we can see it is only a 8 byte big file.

```{shell}
 % ls -lisa mcubootinfo.bin
8632122446 8 -rw-r--r--  1 kai  staff  8 18 Feb 22:35 mcubootinfo.bin
```

First of all we need to find the correct matches for the defines IMG_STATUS_TESTING, IMG_STATUS_TESTREADY, IMG_STATUS_NOTEST.
Remember ARM is little endian based, that means 0xABCDDCBA will become 0xBADCCDAB in our binary.

```{shell}
% r2 mcubootinfo.bin      
 -- A C program is like a fast dance on a newly waxed dance floor by people carrying razors - Waldi Ravens
[0x00000000]> /x badccdab
Searching 4 bytes in [0x0-0x8]
hits: 1
0x00000004 hit4_0 badccdab
[0x00000000]> 
```

And of course we get a macht for this byte. So in this case we will boot our image in NOTEST mode. The selected Image is 0x02 beacuse the first byte is read from the bootloader due to flc.c:

```{shell}
[0x00000000]> x 4
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00000000  02d8 0320   
```

So agian we need to rememeber it is little endian and it is 4 byte aligned so only 0x02 is used, the other bytes seen should be just garbage due to the 4 byte alignment. 

Examples for other modes an images can look like this:

TESTREADY:
```{shell}
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00000000  02d8 0320 6587 7856       
```

TESTING mit Image 0x01:
```{shell}
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00000000  01d8 0320 2143 3412     
```

## Format of Toniebox OFW Image reversed with radare2 

First of all let's start with the interesting informations at the end of the files.
```{shell}
 % r2 mcuimg2.bin 
 -- A git pull a day keeps the segfault away
[0x00000000]> sG
[0x000266e6]> s -2
[0x000266e4]> x -220
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00026608  0300 0000 4555 5f56 332e 302e 365f 4246  ....EU_V3.0.6_BF
0x00026618  312d 3000 4555 5f56 332e 302e 365f 7374  1-0.EU_V3.0.6_st
0x00026628  6162 6c65 5f62 7261 6e63 6800 0500 acbe  able_branch.....
0x00026638  0000 0000 bb1b 4c5e 0000 0000 6161 3232  ......L^....aa22
0x00026648  6236 3200 3138 2046 6562 2031 383a 3135  b62.18 Feb 18:15
0x00026658  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026668  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026678  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026688  0001 0200 0100 010d 0000 0000 0000 0000  ................
0x00026698  0200 0000 0000 0000 0500 acbe 3131 6661  ............11fa
0x000266a8  3362 3832 3733 6237 6530 6439 3837 3131  3b8273b7e0d98711
0x000266b8  3566 6136 6263 3630 3031 6131 6166 3163  5fa6bc6001a1af1c
0x000266c8  6339 3433 3562 3330 3338 3831 3132 3436  c9435b3038811246
0x000266d8  6232 3030 3663 6565 6539 3866            b2006ceee98f
f[0x000266e4]> 
```

It seems we have a creation date, a version number and an hash as well as an git shorthash in the file end.
Let's proof the hash algorithm, assuming we have sha256 because of the given length.


```{shell}
 % r2 mcuimg2.bin
 -- Finnished a beer
[0x00000000]> sG 
[0x000266e6]> s -2
[0x000266e4]> x -160
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00026644  6161 3232 6236 3200 3138 2046 6562 2031  aa22b62.18 Feb 1
0x00026654  383a 3135 0000 0000 0000 0000 0000 0000  8:15............
0x00026664  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026674  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026684  0000 0000 0001 0200 0100 010d 0000 0000  ................
0x00026694  0000 0000 0200 0000 0000 0000 0500 acbe  ................
0x000266a4  3131 6661 3362 3832 3733 6237 6530 6439  11fa3b8273b7e0d9
0x000266b4  3837 3131 3566 6136 6263 3630 3031 6131  87115fa6bc6001a1
0x000266c4  6166 3163 6339 3433 3562 3330 3338 3831  af1cc9435b303881
0x000266d4  3132 3436 6232 3030 3663 6565 6539 3866  1246b2006ceee98f
[0x000266e4]> s 0
[0x00000000]> ph sha256 0x000266a4
11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f
```

Rocks, seems that we have found everything to calculate an valid toniebox hash by our own.
So we can found the following ofsets, relativly to EOF:

- from -160 to -153 the git shorthash
- from -152 to -140 the creation date 
- from -64 to EOF the SHA256 hash of the file

Unfortunately the version string isn't so fix and differs in it's length
see 3.0.6 for example in comparison to version 3.0.7. and 3.0.8

```{shell}
 % r2 mcuimg2.bin
 -- Documentation is for weak people.
[0x00000000]> sG
[0x000266e6]> s -2
[0x000266e4]> x -220
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00026608  0300 0000 4555 5f56 332e 302e 365f 4246  ....EU_V3.0.6_BF
0x00026618  312d 3000 4555 5f56 332e 302e 365f 7374  1-0.EU_V3.0.6_st
0x00026628  6162 6c65 5f62 7261 6e63 6800 0500 acbe  able_branch.....
0x00026638  0000 0000 bb1b 4c5e 0000 0000 6161 3232  ......L^....aa22
0x00026648  6236 3200 3138 2046 6562 2031 383a 3135  b62.18 Feb 18:15
0x00026658  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026668  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026678  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00026688  0001 0200 0100 010d 0000 0000 0000 0000  ................
0x00026698  0200 0000 0000 0000 0500 acbe 3131 6661  ............11fa
0x000266a8  3362 3832 3733 6237 6530 6439 3837 3131  3b8273b7e0d98711
0x000266b8  3566 6136 6263 3630 3031 6131 6166 3163  5fa6bc6001a1af1c
0x000266c8  6339 3433 3562 3330 3338 3831 3132 3436  c9435b3038811246
0x000266d8  6232 3030 3663 6565 6539 3866            b2006ceee98f
f[0x000266e4]> 
```

```{shell}
% r2 mcuimg1.bin 
 -- Select your character: RBin Wizard, Master Anal Paladin, or Assembly Warrior
[0x00000000]> sG
[0x0002841a]> s -2
[0x00028418]> x -220
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x0002833c  0100 0000 0002 0000 5044 5f56 332e 302e  ........PD_V3.0.
0x0002834c  372d 3000 5044 5f56 332e 302e 375f 7374  7-0.PD_V3.0.7_st
0x0002835c  6162 6c65 5f62 7261 6e63 6800 0500 acbe  able_branch.....
0x0002836c  0000 0000 33a2 c75f 0000 0000 3339 6133  ....3.._....39a3
0x0002837c  6166 3700 3032 2044 6563 2031 353a 3138  af7.02 Dec 15:18
0x0002838c  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x0002839c  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x000283ac  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x000283bc  0001 0200 0100 010e 0000 0000 0000 0000  ................
0x000283cc  0300 0000 0000 0000 0500 acbe 6233 3565  ............b35e
0x000283dc  3665 3233 6238 3539 6662 3332 6565 3930  6e23b859fb32ee90
0x000283ec  3838 6562 6231 6130 3961 6165 3363 6163  88ebb1a09aae3cac
0x000283fc  3163 3933 3032 3365 3636 6166 6635 3336  1c93023e66aff536
0x0002840c  6463 6561 3664 3564 3439 3862            dcea6d5d498b
[0x00028418]> 
```

```{shell}
% r2 mcuimg3.bin 
 -- This is an unregistered copy.
[0x00000000]> sG
[0x00027cab]> s -2
[0x00027ca9]> x -220
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00027bcd  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00027bdd  0000 00aa aaaa aa45 555f 5633 2e30 2e38  .......EU_V3.0.8
0x00027bed  2d30 0033 2e30 2e38 5f45 5500 0500 acbe  -0.3.0.8_EU.....
0x00027bfd  0000 0000 fb19 875f 0000 0000 3333 6434  ......._....33d4
0x00027c0d  6633 6100 3134 204f 6374 2031 373a 3332  f3a.14 Oct 17:32
0x00027c1d  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00027c2d  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00027c3d  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00027c4d  0001 0200 0100 010e 0000 0000 0000 0000  ................
0x00027c5d  0200 0000 0000 0000 0500 acbe 6632 6565  ............f2ee
0x00027c6d  3433 3365 3036 3330 6135 3632 3433 3234  433e0630a5624324
0x00027c7d  3237 3764 3736 3363 6533 6337 6165 6131  277d763ce3c7aea1
0x00027c8d  3633 3061 3961 3037 6134 6239 3831 3766  630a9a07a4b9817f
0x00027c9d  3039 3535 3066 3235 6665 3536            09550f25fe56
[0x00027ca9]> 
```

But every version string seems to have the pattern _V included, lets try to build 
an regular expression for it and every version string is followed by the bytes
0500 acbe so far, we could use that to find an start point for our search.

Another very interessting observation are the bytes 0xBEAC0005 at the end of the file just
right before the SHA256 hash.

## Format of Toneibox original bootloader reversed with radare2

```{shell}
% r2 mcuimg.bin
 -- AHHHHH!!!! ASSEMBLY CODE!!!!!! HOLD ME I'M SCARED!!!!!!!!!!
[0x00000000]> sG
[0x000051de]> s -2
[0x000051dc]> x -250
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x000050e2  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x000050f2  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00005102  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00005112  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00005122  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00005132  0000 0000 0000 0000 0000 0000 0000 93c7  ................
0x00005142  0320 b4c7 0320 fac7 0320 e1c7 0320 1dc7  . ... ... ... ..
0x00005152  0320 a6c7 0320 a1c7 0320 8fc7 0320 c6c7  . ... ... ... ..
0x00005162  0320 d9c7 0320 99c7 0320 0500 acbe 0000  . ... ... ......
0x00005172  0000 456d c957 0000 0000 3039 6336 3337  ..Em.W....09c637
0x00005182  3400 4672 6920 5365 7020 2032 2031 343a  4.Fri Sep  2 14:
0x00005192  3135 3a30 3120 4345 5354 2032 3031 3600  15:01 CEST 2016.
0x000051a2  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x000051b2  0000 0000 0000 0000 0000 0000 0000 0001  ................
0x000051c2  0200 0100 0106 0000 0000 100e 0000 0000  ................
0x000051d2  0000 2c01 1000 0500 acbe                 ..,.......
[0x000051dc]> 
```

So as we can see we get the same EOF indicator as within the mcuimgX.bin images.
But it seems like there is no hash stored within the bootloader itself. Won't make
sense at all, because the is no bootstage that could verify the correct hash of the BL.
But we get an git shorthash and an timestamp again.

## Python tool for extracting all this information by your own

During the reversing of all this cool there was a python tool developped for extracting all this information by your own 
if you are afraid for hex editors. It has some nice features like recursive mode, csv and json export so you can extract this informations from any folder you like. For the toniebox users out there who have a big collection of firmware images :)

Find the tool here: [Firmware Information Extractor](https://github.com/toniebox-reverse-engineering/toniebox/blob/master/tools/firmware_info.py)

It is almost self explaining and has a help menue: 

```{shell}
%% ./firmware_info.py -r testfolder/foo


Filename: testfolder/foo/mcuimg2.bin
Firmware Version: 	EU_V3.0.6_BF1-0
Firmware Version: 	EU_V3.0.6_stable_branch

Creation Date: 		18 Feb 18:15

Read SHA256: 		11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f
Calculated SHA256: 	11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f
GIT Shorthash: 		aa22b62


Filename: testfolder/foo/mcuimg3.bin
Firmware Version: 	EU_V3.0.8-0
Firmware Version: 	3.0.8_EU

Creation Date: 		14 Oct 17:32

Read SHA256: 		f2ee433e0630a5624324277d763ce3c7aea1630a9a07a4b9817f09550f25fe56
Calculated SHA256: 	f2ee433e0630a5624324277d763ce3c7aea1630a9a07a4b9817f09550f25fe56
GIT Shorthash: 		33d4f3a


Filename: testfolder/foo/mcuimg1.bin
Firmware Version: 	PD_V3.0.7-0
Firmware Version: 	PD_V3.0.7_stable_branch

Creation Date: 		02 Dec 15:18

Read SHA256: 		b35e6e23b859fb32ee9088ebb1a09aae3cac1c93023e66aff536dcea6d5d498b
Calculated SHA256: 	b35e6e23b859fb32ee9088ebb1a09aae3cac1c93023e66aff536dcea6d5d498b
GIT Shorthash: 		39a3af7
% ./firmware_info.py -jr testfolder/foo
[
    {
        "Filename": "testfolder/foo/mcuimg2.bin",
        "FWInfo": [
            "EU_V3.0.6_BF1-0",
            "EU_V3.0.6_stable_branch"
        ],
        "creationDate": "18 Feb 18:15",
        "git shorthash": "aa22b62",
        "sha256": "11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f",
        "calculatedHash": "11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f"
    }
]
[
    {
        "Filename": "testfolder/foo/mcuimg2.bin",
        "FWInfo": [
            "EU_V3.0.6_BF1-0",
            "EU_V3.0.6_stable_branch"
        ],
        "creationDate": "18 Feb 18:15",
        "git shorthash": "aa22b62",
        "sha256": "11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f",
        "calculatedHash": "11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f"
    },
    {
        "Filename": "testfolder/foo/mcuimg3.bin",
        "FWInfo": [
            "EU_V3.0.8-0",
            "3.0.8_EU"
        ],
        "creationDate": "14 Oct 17:32",
        "git shorthash": "33d4f3a",
        "sha256": "f2ee433e0630a5624324277d763ce3c7aea1630a9a07a4b9817f09550f25fe56",
        "calculatedHash": "f2ee433e0630a5624324277d763ce3c7aea1630a9a07a4b9817f09550f25fe56"
    }
]
[
    {
        "Filename": "testfolder/foo/mcuimg2.bin",
        "FWInfo": [
            "EU_V3.0.6_BF1-0",
            "EU_V3.0.6_stable_branch"
        ],
        "creationDate": "18 Feb 18:15",
        "git shorthash": "aa22b62",
        "sha256": "11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f",
        "calculatedHash": "11fa3b8273b7e0d987115fa6bc6001a1af1cc9435b3038811246b2006ceee98f"
    },
    {
        "Filename": "testfolder/foo/mcuimg3.bin",
        "FWInfo": [
            "EU_V3.0.8-0",
            "3.0.8_EU"
        ],
        "creationDate": "14 Oct 17:32",
        "git shorthash": "33d4f3a",
        "sha256": "f2ee433e0630a5624324277d763ce3c7aea1630a9a07a4b9817f09550f25fe56",
        "calculatedHash": "f2ee433e0630a5624324277d763ce3c7aea1630a9a07a4b9817f09550f25fe56"
    },
    {
        "Filename": "testfolder/foo/mcuimg1.bin",
        "FWInfo": [
            "PD_V3.0.7-0",
            "PD_V3.0.7_stable_branch"
        ],
        "creationDate": "02 Dec 15:18",
        "git shorthash": "39a3af7",
        "sha256": "b35e6e23b859fb32ee9088ebb1a09aae3cac1c93023e66aff536dcea6d5d498b",
        "calculatedHash": "b35e6e23b859fb32ee9088ebb1a09aae3cac1c93023e66aff536dcea6d5d498b"
    }
]
```