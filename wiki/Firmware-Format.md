# Analysing the toniebox firmware image format


## Format of Tonibox OFW Image reversed with radare2 

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

So you can find an simple python tool for extracting all information from firmware files
here: [Firmware Information Extractor](https://github.com/toniebox-reverse-engineering/toniebox/blob/master/tools/firmware_info.py)