# Debug Port
## Position of debug port on Toniebox-PCB

![https://github.com/toniebox-reverse-engineering/toniebox/blob/master/pics/toniebox_pcb_debug_port.png](https://github.com/toniebox-reverse-engineering/toniebox/blob/master/pics/toniebox_pcb_debug_port.png)

The debug port runs on `3.3 V`

## Layout debug port
```
  10 9 8 7 6 
   1 2 3 4 5  
```

![https://github.com/toniebox-reverse-engineering/toniebox/blob/master/pics/debug_port_pin_out.png](https://github.com/toniebox-reverse-engineering/toniebox/blob/master/pics/debug_port_pin_out.png)


| Pin | Function | Comment               |
| --- | -------- | --------------------- |
| 1   | TX       | 55                    |
| 2   | RX       | 57                    |
| 3   | VCC      | 3.3V                  |
| 4   | RST      | 32                    |
| 5   | GND      |                       |
| 6   | ?        | 45                    |
| 7   | TCK      | 19                    |
| 8   | TMS      | 20                    |
| 9   | SOP2     | 21 (indirect SOP0 35) |
| 10  | ?        | U3                    |

# Tag-Connector for debug port

To connect to the debug port a Tag-Connector can be used.

Datasheet: [Tag Connect TC2050-IDC-NL]https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/TC2050-IDC-NL_Datasheet_8.pdf)

Available at: [Tag Connect TC2050-IDC-NL](https://www.tag-connect.com/product/tc2050-idc-nl-10-pin-no-legs-cable-with-ribbon-connector)

# Boot Mode
The CC3200 device implements a sense-on-power (SoP) scheme to switch between two modes that are available within the Tonie project. (To switch between the boot modes a restart of the device is needed.) [CC3200 datasheet 5.9.3](http://www.ti.com/lit/ds/symlink/cc3200.pdf)
## SWD Mode
SOP2 (pin 9) low will activate the functional mode with a 2-wire SWD mapped to TCK (pin 7) and TMS (pin 8) of the debug port 
## UART mode
SOP2 (pin 9) high will activate the UART load mode to flash the system during development and in OEM assembly line

# Extract Firmware
To activate UART Mode, SOP2 (pin 9) needs to be pulled high.
## Introduction
Grab your favourite USB-UART 3.3V interface, recommending those with DTR and RTS port to automate board reset + boot mode (SOP2 / pin9 = high). You may also use a CC3200 Launchpad, but then you will need to reset it by hand.
## Toolset
Use [cc3200tool](https://github.com/toniebox-reverse-engineering/cc3200tool) to extract the firmware.
1. Extract full firmware `cc3200tool -p /dev/ttyUSB2 --sop2 ~dtr --reset rts read_flash firmware.dmp`
2. List files in FatFS `cc3200tool -p /dev/ttyUSB2 --sop2 ~dtr --reset rts list_filesystem`
3. Extract the files you like `cc3200tool -p /dev/ttyUSB2 --sop2 ~dtr --reset rts read_file /sys/mcuimg.bin ./sys/mcuimg.bin`

<!--
 # SWD debug mode
 By pulling SOP2 (pin 9) low, SWD debug mode on TCK (pin 7) and TMS (pin 8) can be activated.

 (...SWD mode needs to be verified. NOT TESTED YET!)
-->

# Log output
The original bootloader and the original firmware do some logging to the serial port with baudrate 921600
ex. "screen /dev/ttyUSB0 921600"

## bootloader
```
CC3200 bootloader v1472818501 (09c6374) build: Fri Sep  2 14:15:01 CEST 2016 dl:1.2.0 sl:1.0.1.6 hw:tb-smt-16:1:13
loaded battery critical level = 3600
battery_level = 4823
```
## original firmware
```
QO      (�72-�3�]FWc041b2f13 Nov 17:47E�3�]Jc041b2f0.   (�2EU_V3.0.5-0E�3�]Jc041b2f<:   (�2EU_V3.0.5_stable_branchE�3�]Jc041b2f+)        (�92E�3�]&  (#2E�3�]]Jc041b (2SPE�3�]%#E�3��        2�
                                                  SP���E�3�]#!  �
                                                                  (�/�E�3�]20   �
                                                                                  (<2�E�3�]20   � (=2�
2%�80USDS�(�5\E�3�]#!E�3� (�9-�z[E�3�]  � (�72E�3�]@>   � (�
94E36D679CD9E�3�]#!     � (�/��E�3�]#!E�� (�/��E�3�]/�E�� (�02�E�3�]2�3�� #(�02-E�3�]#! � (�/�E�3�]#!   � (�/�E�3�]#!   �  (�/��E�3�]#! �! !(�0E�3�]#!      �" !(�0E�3�]    �# (�2E�3�]     �$ (�02E�3�]    �% (�&2�E�3�]   �& (�&2;E�3�]   �' (�&2�)E�3�]! �( (�&2�)NE�3�] �) (�&2�E�3�]       �* (�&E�3�]#!   �+ (�&@'|E�3�]  �, #(�02-E�3�]  �- (�72E�3�]#!  �. (�5`E�3�]    �/ (�2E�3�];9   �0 (�
1 (�22"content/00000001/00000000\���E�3�]#!     2 (�u��WE�3�]#! 3 (�9\�E�3�]'%  4 (�52E�3�]     5 (�52E�3�]#!2 E6 (�5u��WE�3�]  ;7 (�62�E�3�]       �8 (�%2E�3�]<:  9 (�2!prod.de.tbs.toys49�E�3�];9        �: (�
                                                                     2 E�3�]    �; (�2E�3�]     �< (�52E�3�]    = (�22\
                                                                                                                       E�3�]    ]> (�22E�3�]#!      ]? (�/�E�3�]/-  ]@ (�/2�E�3�]   ^A (�2E�3�]#!   ^B (�/��E�3�]   �C (�%2E�3�]20  �D (Z2E�3�]20   �E (<2�
/E�3�]20        �F (=2�
                       E�3�]MK  (G (�22SPGETprod.de.tbs.toys�/v1/ota/4?cv=33545114E�3�]86       �H %(�2rtnl.bxcl.de�L8�E�3�]EC  �I (h2+prod.de.tbs.toys�/v1/ota/4?cv=33545114E�3�]  �J (�82�E�3�]#! 0K (�8�JE�3�]53  L (�>2Fritz!Box 75905037E1B7F880����E�3�]'%  "-M %(�:2QE�3�]QO       #-N(�72-�3�]FWc041b2f13 Nov 17:47E�3�]Jc041b2f0.    $-O(�2EU_V3.0.5-0E�3�]Jc041b2f<:        %-P(�2EU_V3.0.5_stable_branchE�3�]Jc041b2f+)    &-Q �� 8�E�3�].,(�02/qT (�02_B$ 8�E�3�].,�020qU (�02_�� 8�E�3�]0.   1qV (�
                                                                      2D8�E�3�]
```