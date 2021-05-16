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