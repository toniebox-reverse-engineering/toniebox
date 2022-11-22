# SD card extension
For convenience a SD extension cable can be used to place the card in a better accessible way. A 25 cm cable is recommend.

You can use both types of cables:

* microSD card – microSD card
* microSD card – SD card

![](https://raw.githubusercontent.com/toniebox-reverse-engineering/toniebox/master/pics/sd_extension_cable.jpg)

## Tools needed:
- Philips screwdriver (PH0)
- flat screwdriver
- soldering station
- double sided foam tape (made for outside use since they are the strongest)
- cutting pliers
- extension cable - minimum 25 cm long (i.e. https://www.amazon.de/B0731FWRZC/) 

## Step 1: Preparing the extension cable

- Remove the plastic casing of the female end of the cable (where the card has to be inserted)
- Remove one resistor on the slot's PCB 

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic01.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic02.jpg)

- Cut the corners of the PCB. Do not cut more than the holes allow as there are electrical traces nearby.

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic03.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic04.jpg)

## Step 2: Open the Toniebox

I won't go into too many details at this step. I believe the following Youtube videos will give all the needed info: https://youtu.be/GOZRjaEhrcQ & https://youtu.be/eiMxkXM8YDs
In order to avoid damaging the PCB, disconnect the battery.

## Step 3: Connecting the extension cable to the mainboard

This part might be a bit tricky on older boards since these ones have a capacitor that sits a few mm in front of the microSD slot. 

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic05.jpg)

Because the male end of the extension cable is not flexible, inserting it in the microSD slot is a matter of force. Before inserting the extension cable it is advisable to check the position of the latch in open and closed state, in order to get a feeling about how much it has to be pushed.

- Open the slot by pushing it towards the capacitor
- Take the original card out and replace it with the extension cable
- Close the microSD slot and simultaneously press with one finger on the latch while locking it into place with a flat screwdriver.
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic09.jpg)

## Step 4: Glue the new microSD slot in an accessible place

- Take as much tape as you feel comfortable (I could have probably added double as much) and stick one side to the cable's microSD slot.
- Glue the slot between the two screw holes on the battery holder, making sure that it sits as close to the edge as possible.

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic10.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic11.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic12.jpg)

- In order to make the slot reach the very edge of the battery holder, some have cut some small slits into the walls of the two screw guides. I wanted to keep the box 100% original so I skipped this step.

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic13.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic14.jpg)

## Step 5: Start putting the box back

- Start by twisting the extension cable in such a way that it could stay between the PCB and the battery holder.
- Screw together the battery holder, the board and the white holder. 
- Make sure the cable sits comfortably under the battery holder

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic15.jpg)

- Power on the box and test that the box recognizes the microSD card
Make sure to never touch the battery release latch, as this will partially detach the microSD slot.

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic16.jpg)

Step 6: Finish putting the box back and test again

- Just make sure that the microSD card is reachable with a set of tweezers and you can comfortably remove and put back the card. Be careful not to drop the card inside the box.

![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic17.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic18.jpg)
![](https://github.com/danieldur/toniebox/blob/master/pics/microSD-extension-cable/pic19.jpg)
