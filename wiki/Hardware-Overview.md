# Pictures (r1)
## Board
![](https://d3nevzfk7ii3be.cloudfront.net/igi/d4ypF2sLF5VkOXXv.medium)

Detail pictures see [iFixit Teardown](https://de.ifixit.com/Teardown/Toniebox+Teardown/106148)

# Parts
## Processor [TI CC3200](http://www.ti.com/lit/ds/symlink/cc3200.pdf)
[Technical Information](http://www.ti.com/lit/ug/swru367d/swru367d.pdf)
Cortex-M4 arm7e-m thumb

I suggest to get a [CC3200 Launchpad](http://www.ti.com/tool/CC3200-LAUNCHXL) for first contact.

![](http://www.ti.com/diagrams/cc3200-launchxl_cc3200-launchxl_no_bg_resize.jpg)

Various useful pins (SOP2, TCK, TMS, GND, RST, GND, RX0, TX0) are available through the onboard debug pins.
## Flash 4MB [ISSI IS25LQ032B](http://www.issi.com/WW/pdf/25LQ080B-016B-032B.pdf)
Firmware is stored in a TI propiertery  FatFS but can easily be read over the RX/TX lines of the mainboard when the CC3200 is in flash-mode.

## Audio DAC [TI TLV320DAC3100](http://www.ti.com/lit/ds/symlink/tlv320dac3100.pdf)
I2C address should be 0x18.
## RFID Reader [TI TRF7962A](http://www.ti.com/lit/ds/symlink/trf7962a.pdf)
Reading MiFare Classic is not possible without using the chips direct mode which means more work. 
1.2 http://www.ti.com/lit/an/sloa248b/sloa248b.pdf 
http://www.ti.com/tool/TRF796X_TRF7970X_MIFARE_12_2013

Firmware TRF7970ABP: http://www.ti.com/lit/zip/sloc297
Example Salae Logic SPI http://www.ti.com/lit/zip/sloc240
## Acceleration Sensor [NXP MMA8451Q](https://www.nxp.com/docs/en/data-sheet/MMA8451Q.pdf)
[Arduino Library](https://github.com/sparkfun/SparkFun_MMA8452Q_Arduino_Library) exists.
I2C address is 0x1D
## RGB LEDs
### Green PIN 21 (SOP2)
### Red PIN 19 (TCK)
### Blue PIN 17 (TDO)