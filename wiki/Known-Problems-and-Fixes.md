# Toniebox related
## Box has a wifi password
### Checks
Does "www.wipy.io" or "TeamRevvoX" work? You may remove the password by connecting to the Box' WiFi, go to http://192.168.1.1/main.html "Device Config" - "Access Point config", set the security type to "Open" and hit apply. Now the password should be removed.

## Box only works on the charger
### Checks
* Battery plugged in?
* Battery defect?

## Hitting the box for skipping tracks doesn't work
### Checks
* Disabled in the cloud?
* Other?

## Box gets (very) hot on the charger, works on battery (if still charged)
### Checks
* Diode near the power connector defect? (D4)
### Reason
The box was plugged into power supply with more than 9V.

## Box detects no figures
### Checks
* XTAL X2 defect?

## Weak WiFi Signal
### Checks

## Box doesn't have a voice, only sounds
### Checks
* microSD defect?

## Blinks red when woken up or a tonie is placed on
### Checks
* microSD defect?

# cc3200tool related
## raise CC3200Error("rx csum failed")
### Checks
* Ground ok?
* Toniebox is getting enought power (an UART 3.3V might not be an apropiate power source for it.)
### Solutions
* Power the toniebox via its battery and/or charger and disconnect the 3.3V connection.
* Use shorter wires (Jumpers and/or USB)
* Use a different USB port (possibly without an USB-hub)

## read_all_files only dumps a few files / list_filesystem has no filenames
If list_filesystem doesn't show the filenames for several or all files on the flash, the tool cannot dump the files automatically with the command read_all_files.
### Solutions
* Dump every [important file](https://github.com/toniebox-reverse-engineering/toniebox/wiki/Firmware-Format#Important-Toniebox-firmware-files) one by one using the read_file command. You may need to create a **cert/** and **sys/** subdirectory in your target dir.
```
python cc.py -p COM3 read_file /cert/ca.der cert/ca.der read_file /cert/private.der cert/private.der read_file /cert/client.der cert/client.der read_file /sys/mcuimg.bin sys/mcuimg.bin read_file /sys/mcuimg1.bin sys/mcuimg1.bin read_file /sys/mcuimg2.bin sys/mcuimg2.bin read_file /sys/mcuimg3.bin sys/mcuimg3.bin read_file /sys/mcubootinfo.bin sys/mcubootinfo.bin
```