# Boot Process

## Introduction
When the CC3200 is started the integrated bootloader is loading /sys/mcuimg.bin from flash to the memory address 0x20004000. The SRAM is located at 0x20000000 to 0x2003FFFF. If you want to implement a second stage bootloader you would usally implement a relocator that moves your bootloader to 0x2000000. If it bootloader smaller than 16kB (0x4000) you then may load your desired firmware from SD or Flash to 0x20004000 as the integrated bootloader would do. The toniebox's (seconds stage) bootloader is bigger than 16kB. So loading it to 0x20000000 wouldn't work.

## Relocator
The original firmware bootloader has a relocator which loads the bootloader to memory address 0x20038000, which 32kB before the very end of the memory. 

## OFW bootloader
The bootloader loads a file called "/sys/mcubootinfo.bin" that contains the id of the firmware to load.

To verify the integrity of the firmware, a sha256 hash is appended to the end of each firmware file. The bootloader checks it.