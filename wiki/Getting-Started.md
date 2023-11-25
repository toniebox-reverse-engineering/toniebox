[Zum Inhalt springen](#content "Zum Inhalt springen")

<div class="inside-header grid-container grid-parent">

<div class="site-branding">

[Gambrius Tech Blog](https://gt-blog.de/)

A loose collection of tech topics

</div>

</div>

<div class="inside-navigation grid-container grid-parent">

<span class="mobile-menu">Menü</span>

<div id="primary-menu" class="main-nav">

  - [Impressum](https://gt-blog.de/impressum/)
  - [Datenschutzerklärung](https://gt-blog.de/datenschutzerklaerung/)

</div>

</div>

<div id="page" class="site grid-container container hfeed grid-parent">

<div id="content" class="site-content">

<div id="primary" class="content-area grid-parent mobile-grid-100 grid-75 tablet-grid-75">

<div id="main" class="site-main" role="main">

<div class="inside-article">

# Toniebox Hacking – How to get started

<div class="entry-meta">

<span class="posted-on">6. Juli 202329. Dezember 2022</span>
<span class="byline">von
<span class="author vcard" itemprop="author" itemtype="https://schema.org/Person" itemscope="">[<span class="author-name" itemprop="name">Gambrius</span>](https://gt-blog.de/author/gambrius/ "Alle Beiträge von Gambrius anzeigen")</span></span>

</div>

<div class="entry-content" itemprop="text">

![](https://gt-blog.de/wp-content/uploads/2022/12/Boxine_Toniebox_hack-1024x512.jpg)

Over the last three years we, the Team RevvoX (formed in Nov. 2019) came
up with a lot of information regarding all the possibilities that can be
done with [Tonieboxes](https://amzn.to/3vozwNI) besides the origin
features.

We achieved to bring, own content, own NFC tags, customization and even
some hardware mods to the Toniebox. In addition we have supported a lot
of repairs for otherwise ‘dead’ boxes with our knowledge of the
different revisions of the PCB to check or exchange the right components
(we even have a [complete reverse engineered hardware
layout](https://github.com/toniebox-reverse-engineering/toniebox-pcb)
within our wiki).

Within this Blog Post I would like to give a short introduction to all
new community members that are interested in tinkering with the new toy
that their children got for Christmas or any other occasion.

<span id="more-662"></span>

You can find all members of the Team RevvoX within our [Telegram
Group](https://t.me/toniebox_reverse_engineering_upd). We are looking
forward to see you there and are more than willing to answer your
questions if there is anything left open.

## **What can be done without any FW or HW modification?**

There are several different levels how to modify the Toniebox and the
user’s experience without changing the hardware or the firmware.

### **Custom Content on the Toniebox**

We as Team RevvoX introduced a software called
[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases),
which is a GUI based Software for Windows that lets you add your own
audio content to any Toniebox independently from the Tonie Cloud.
Therefore, you can grab some mp3 files and encode them as TAF (Tonie
Audio File) and implement them on the build-in microSD Card of the
Toniebox.

This can be done just by getting access to the microSD card and placing
this into any microSD card reader on the PC.
[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
will recognize all Contents that are already stored / downloaded to the
box. After encoding some own audio content you can place the card back
into the Toniebox and it will work.

No firmware modification nor other hardware hacks needed.

### **Custom NFC tags**

To let the Toniebox play your own content, you need to have some way to
let the box know what it should play. Therefore we figured out, what
kind of NFC Chip is used within the figurines and how it is linked to
the box and its content. If you like to understand how this works,
please feel free to read one of my older blogs dedicated to the
internals ([click here](https://gt-blog.de/custom-tags-for-toniebox/)).

By using custom tags you can let your box play your custom content.

[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
helps you to get the link between the custom tag and your custom audio
content set. For this you need the 8 Byte long UID of your custom
tags.  
There are several ways to read the UID of the custom tags, such as using
smartphone apps (iOS: [NFC
Tools](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwj3ueKe15T8AhV3iv0HHVa6CxIQFnoECBsQAQ&url=https%3A%2F%2Fapps.apple.com%2Fde%2Fapp%2Fnfc-tools%2Fid1252962749&usg=AOvVaw1ySJiyPJUVQU_mwhKNCpJa),
[NXP Tag
Info](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi5g6KQ15T8AhV0i_0HHfXLCEwQFnoECBQQAQ&url=https%3A%2F%2Fapps.apple.com%2Fde%2Fapp%2Fnfc-taginfo-by-nxp%2Fid1246143596&usg=AOvVaw0B_aRikk83iOJMSujKASuk);
Android: [NXP Tag
Info](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiw8Njf15T8AhUW77sIHcxWC74QFnoECCkQAQ&url=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.nxp.taginfolite%26hl%3Dde%26gl%3DUS&usg=AOvVaw2ggWCzi10d5GEp4U_ilawX)),
hardware tools like the Proxmark3 or the Flipper zero, or an Arduino
with a compatibel NFC reader (e.g. ESP8266 with a PN5180).

IMPORTANT: Once the tag is placed on the Toniebox you will NOT be able
to read the UID of the custom tags because the Toniebox will enable the
“privacy mode” on this tag. What this is and how to get out of this
mode, you can read in the section “Important things to know” further
down this Blog post.  
The solution to this is FIRST read ALL UIDs from your custom tag, write
them down and then start using them with the Toniebox.

#### **Where can I get the right custom tags that will work with my Toniebox?**

\[**RFIDfriend**\] is the answer and the recommend source by Team
RevvoX\! He spent a lot of time and effort figuring out where to get the
right tags and was able to source some of these. By going back and forth
with some Chinese RFID label manufactures and buying a lot of wrong NFC
tags, he was eventually able to get his hands on the right ones. They
come in form of round labels with a diameter of 38mm.  
RFIDfriend has some of these tags left and is more than willing to hand
these over to some tinkerers. You can find him on
[Kleinanzeigen](https://www.kleinanzeigen.de/s-anzeige/rfid-tag-fuer-toniebox-original-nxp-icode-slix-l-rfidfriend/2456639376-23-3480),
or can contact him directly via [Telegram Chat](https://t.me/RFIDfriend)
or via [eMail](mailto:RFIDfriend@gmail.com) (he sends these
international as well).  
Be aware that there are some Chinese fakes going around as well\! These
tend to fail after minimal use. But you can be assured that RFIDfriend
is only handling tags with the original NXP chip build in.

### **Play original content with custom tags**

The way the Toniebox works is that as soon as a figurine is placed on
top of the box, it checks whether the related content is already on the
internal microSD card and starts to play it back, or it starts
downloading the corresponding audio content from the Tonie Cloud and
saves this on the microSD card while it starts playing it back.

While there are many possibilities to exchange these figurines with
friends, from the kindergarten or even from public libraries, the
content will remain on the microSD card of your Box even if the
figurines are returned to their owners.

[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
can identify the content on your microSD card and you can relink this to
custom tags. This allows you to play the original Tonie audio content
even if you no longer have the original figurine on hand.

Within
[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
you just do a simple double click on the identified content and it will
open a popup window that shows the UID of the original Tonie figurine to
that the audio content is linked to. You can now edit this UID to the
UID of your custom tag. That’s all it takes to continue playing the
content that has already been downloaded to your Toniebox.

In case you are interested in the legal matter: In Germany, Austria and
Switzerland, this is called
“[Privatkopie](https://de.wikipedia.org/wiki/Privatkopie)” and is
covered by relevant law.

### **Downside of going the custom content / custom NFC tag way**

There is just one downside to this. You have to keep the box in Offline
Mode, or just cut off the internet connection for your Toniebox via your
internet router settings.

Every time the box starts up it is verifying the whole content that is
stored on the internal microSD card with the Tonie Cloud. This is
eventually leading to the deletion of content that is not linked to UIDs
known to the Tonie Cloud when the according custom tag is placed on top
of the box (while this is online). Even the unplayed custom content is
changed so that the resume feature will not work for it anymore, even
after switching back to Offline Mode.

Why exactly this takes place and how you can get away with the Offline
Mode and live with this while still using original Tonie figurines, you
can find in the section further down in this article about the
“important things to know”.

## **What can be done with Bootloader / FW modification?**

The PCB design of the Toniebox has a Debug Connector present. This
arouses even more curiosity about going further down that rabbit hole.
In this section I will just briefly explain what can be done so far.  
If you are interested in how to make a full dump of the flash, take a
look into my [older blog post](https://gt-blog.de/toniebox-firmware-dump/) where I explain in
detail how to do this.  
Information about how to [install the custom bootloader](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install),
please take a look into our
[wiki](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install).

IMPORTANT: As of now only the Toniebox V1 and V2 are able to get the
[Bootloader / FW mod](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install).
The V3 uses another microcontroller and is not yet ready for this. We
are working hard on this…

### **Custom Bootloader / HackieboxNG SD bootloader**

The [Bootloader](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install)
is the first thing that gets started when the microcontroller gets
powered up. It takes care of preparing some basic stuff AND will
eventually load the Toniebox firmware.

The [HackieboxNG SD bootloader](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install)
enables two main features to the user:

  - switch between different firmwares (up to nine OFWs and CFWs)
  - patching the original firmware on startup

#### **Switching between different firmwares**

By pressing the ear buttons in a certain order, the box will prompt you
with a different blinking sequence at the center light, signaling that
you are in the FW switching mode. Here you can switch between nine
firmware slots. These can be either different versions of the original
firmware or could be [custom
firmware](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install)
(see next section).

#### **Patching the original firmware on startup**

With patches for the original firmware you can add certain features to
the normal use of your Toniebox. To name a few:

  - disable privacy mode  
    the privacy mode for the figurines and custom tags will remain
    disabled after removing them from the box
  - disrupt the connection to the Tonie Cloud
  - use of alternative NFC tags  
    enables the use of other NFC standards in addition to the one
    demanded by the Toniebox
  - disable hidden mode  
    blocks the verification at the start of the content directory with
    the cloud. This way, the custom content will not get the “hidden
    flag” (see section “important to know”)
  - …

More details and How Tos can be found in our
[wiki](https://gt-blog.de/custom-tags-for-toniebox/).

### **Custom Firmware (CFW)**

[The custom
firmware](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng/wiki/Install)
(CFW) by Team RevvoX is as of now just a proof of concept and not able
to serve as a daily use firmware for the Toniebox.  
You can play single WAV files and see differnt hardware status within a
webpage that is provided. Even a file transfer is possible (that is far
too slow to use it as a content handler).

If my words did not hold your interest and you like to support further
development to a useable solution that is capable to play TAFs, please
visit our
[wiki](https://github.com/toniebox-reverse-engineering/hackiebox_cfw_ng)
for more information.

## **What hardware hacks can be done?**

### **relocation of microSD card reader**

Because managing the content on the microSD card with
[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
requires regular access to the microSD card, and a complete teardown of
the Toniebox would take some time (although we did [some speedruns to
proof how fast we are](https://www.youtube.com/watch?v=GOZRjaEhrcQ)), we
came up with a simple hardware modification that lets you relocate the
microSD card holder to the bottom of the Toniebox just behind the lid.

For this mod you would need a microSD card extension which is at least
25cm long (longer than that is fine, there is enough space within the
Toniebox to place longer cables).

Here are some Amazon Links to the needed extension. (some of them are
now and then not available. Thats why I pasted some more links).

  - [Amazon Lin](https://amzn.to/3WM9gsr)k – 25cm
  - [Amazon Link](https://amzn.to/39Slucz) – 25cm
  - [Amazon Link](https://amzn.to/3PVlcG4) – 48cm (choose the TF – TF option)
  - [Amazon Link](https://amzn.to/3vjmeCi) – 48cm
  - [Amazon Link](https://amzn.to/3WNJLa1) – 48cm
  - [Amazon Link](https://amzn.to/3C98td7) – 48cm
  - [Amazon Link](https://amzn.to/3G75gw2) – 60cm
  - [Amazon Link](https://amzn.to/3WQOWpG) – 60cm

If you like to procure a ready modified cable where the housing and the
resistor is removed, please take a look at [this offer](https://www.ebay-kleinanzeigen.de/s-anzeige/microsd-auf-microsd-verlaengerung-extension-sd-toniebox-teddybench/1550563864-225-1584).

Here are some Pics that show how the mod is done. A detailed write up is
in the making.

![](https://gt-blog.de/wp-content/uploads/2022/12/SD_extension.jpeg)

![](https://gt-blog.de/wp-content/uploads/2022/12/HW_mod_-_SD_relocation_4-1-1024x768.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/HW_mod_-_SD_relocation_3-768x1024.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/HW_mod_-_SD_relocation_2-768x1024.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/HW_mod_-_SD_relocation_6-768x1024.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/HW_mod_-_SD_relocation_5-576x1024.jpg)

Quick HowTo: remove black plastic housing of extension; remove red
marked resistor from extension PCB (e.g. with plier); make two small cut
outs in the screw studs; slide extension PCW in between the studs; use
some hot glue to fix the PCB; take care that when the microSD card is
inserted the upper side of the card is slightly higher than the
surrounding surface (this way you can press it and it will come up to
grab it with your fingers).

The red marked resistor needs to be removed. Otherwise the Toniebox will
not be able to read the microSD card\!

Inserting the microSD card extension into the microSD card holder on the
PCB takes a bit of gentle force. There is one larger (silver
cylindrical) part right next to the holder. But if you give a bit
pressure on the whole package you will be able to close the lid of the
microSD card holder.

### **Build your own figurines and tags**

The original figurines are definetly an outstanding feature of the
Toniebox. My kids love to play with these even without the Toniebox. But
sometimes they are very bulky as well. Especially while traveling.
Therefore I came up with the “Travel Tonie”. It is a coin shaped custom
tag that includes a picture of the original figurine, a magnet and a NFC
tag from RFIDfriend (the round sticker). This way we are able to bring
much more Storys with us on our journeys.

Here are some Pics that show how these tags are build up. A detailed
write up is in the making.

![](https://gt-blog.de/wp-content/uploads/2022/12/coin_tag_1-1024x768.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/coin_tag_5-1024x768.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/coin_tag_6-1024x768.jpg)

![](https://gt-blog.de/wp-content/uploads/2022/12/coin_tag_2-1024x768.jpg)

I used the following coin cases and magnets:

  - [Amazon Link](https://amzn.to/3VpqoDj) – Coin Case (40 mm) 100 pcs
  - [Amazon Link](https://amzn.to/3Wx7NXh) – Coin Case (40 mm) 40 pcs
  - [Amazon Link](https://amzn.to/3GqficO) – magnets (10 x 3 mm)
  - [custom tags from RFIDfriend](https://www.ebay-kleinanzeigen.de/s-anzeige/original-nxp-icode-slix-l-rfid-tag-rfidfriend-toniebox/1995088030-168-3480)

## **What else is possible?**

### **Support of Proxmark3**

The Proxmark3 is a powerfull NFC / RFID / hacking device. But at that
point of time when we were trying to read the NFC tags build in the
Tonie figurines, it was not able to read tags where the “Privacy Mode”
was enabled.  
Thats why we came up with a firmware mod, that would add three Toniebox
related features:

  - disable privacy mode at tonie figurines / custom tags (with known
    passwords)
  - communicate with [TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
  - emulate NFC tags for the Toniebox

**Use TeddyBench with the support of Proxmark**3

[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
can change the linked UID of the audio content on the microSD card. This
can be done by double clicking on the audio content to be changed. A
window will open and present the actual linked UID which can be edited.
This can be either done by manually enter the new UID via the keyboard
(the UID must be read prior to this with your smartphone app), or you
could just place the tag onto the Proxmark3, which will disable the
privacy mode and enter the UID for you.

In addition it will show you the linked content within the Content frame
of [TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases).
If you place any used tag onto the Proxmark3, it will directly highlight
the linked content so that you know immediately what this tag is
connected to at the moment.

**Here are some links to get your hands on the Proxmark3**

  - [Amazon link](https://amzn.to/3Ia81iC)
  - [Amazon link](https://amzn.to/3WOzEBX)
  - [Amazon link](https://amzn.to/3WMS1Hw)
  - [Amazon link](https://amzn.to/3PYbzGu)
  - [Amazon link](https://amzn.to/3PVNQXC)
  - [Amazon link](https://amzn.to/3VtcQ9B)
  - [Amazon link](https://amzn.to/3vkL8RW)
  - [Amazon link](https://amzn.to/3YYIBuu)
  - [Amazon link](https://amzn.to/3YS5JdZ)

#### **Emulating Tonies using Proxmark3**

The NFC tags used for the Toniebox store in total 40 Bytes of data. 8
Byte are used for the UID and 32 Bytes are stored within the memory
blocks (8 Blocks á 4 Bytes).  
With the Dump feature build into
[TeddyBench](https://github.com/toniebox-reverse-engineering/teddy/releases)
you can use the Proxmark3 to read the complete data from tags. This data
can be used to emulate a NFC tag. When the Proxmark3 is placed on top of
the Toniebox and you start the emulation feature with the prior read 40
Bytes of data, the Proxmark3 starts emulating the given information and
the Toniebox starts playing the connected audio accordingly.

### **Emulating Tonies with Flipper zero**

For the Flipper Zero our Team Member g3gg0 came up with an addition to
enable it to read iso15693 tags although the used internals are not
capable of doing so. He bitbanged the needed protocol into the tool and
added the feature of dumping tonie figurines / tags. An emulation
feature was added as well, where the prior dumped information could be
used to play these back and the Flipper zero could be placed on top of
the Toniebox which will start working the same way as the original tag
would do.

You will find more information on [g3gg0s blog](https://www.g3gg0.de/wordpress/rf/flipper-zero-for-toniebox-figurines/).

## **Important things to know**

Some hints on common issues and failiures that can be done:

### **Offline Mode**

If you have custom content on your microSD card, or you have linked
original content to custom tags, you should avoid going online with your
box. Otherwise two things will happen to your custom stuff. For all
custom stuff the resume feature will get lost and if you place your
custom tag on the box while it is online, it will delete this content as
well.

To avoid this you could either switch to the Offline Mode (holding both
ears until a sound is played, press one of both ears again until another
sound is played), or you could take some actions like blocking the
Toniebox within your router. Linking the Box to a Wifi that is only
active when needed, works as well.

I for myself use a second microSD card to download new content with
original Tonie figurines and copy the new files to another microSD card
that I only use in Offline Mode. This way I can have fun of both worlds.

BUT BE AWARE: The Box will leave the Offline Mode as soon as it gets
disconnected from the battery, or the battery runs flat.

### **Resume feature / Live mode / hidden file attribute**

If your box goes Online while having your custom stuff on it, the
Toniebox will add the “hidden” file attribute to the files that are
altered / not known to the Tonie Cloud. Although you did not place the
custom tag on the Toniebox (this would let the box delete this specific
content) before you went back Offline, it enables the “LIVE Mode” (just
ment for creative tonies). This means that the audio will ALWAYS play
from the very beginning and the resume feature will not work.

You will get this feature back by removing the “hidden file attribute”
from all custom content files. The better way is to keep the box from
going online. Or take care that the microSD card with the custom content
is not going online and you always use a different microSD card to go
online and download new content (see Offline Mode section for more
information).

### **Privacy Mode – What is it and how do I get rid of it?**

The NFC chips used within the Tonie figurine are keeping their
information as a secret. They are locked into a so called “privacy mode”
that can only be disabled by using the password set by boxine.

The custom tags you can buy from RFIDfriend are send to you with a
disabled privacy mode. That means you can read the UID with you
smartphone and tools like “NFC Manager” or “NXP Tag Info”. But as soon
as these were placed on the Toniebox, these will be locked as well.

To disable the privacy mode you could either use a Proxmark3 or use the
“knock method”.  
The knock methode is called so, because you “knock” (or tab) the tag or
the figurine very quickly onto the reader surface of the Toniebox and
remove it immediately. This way the box will disable the privacy mode
and tries to read the content of the chip. The quick remove of the tag
from the reader prevents the box to enable the privacy mode again.

If it does not work for you, you might be toooo slow. Here is a short
[video](https://youtu.be/IiZYM5k90pY).

### Toniebox hardware differences – V1, V2, V3

The first Toniebox was released at the second half of 2016. Since then
two major PCB layout changes were released.

The V1 and V2 share basically the same architecture around the TI CC3200
microcontroller. The V2 was released during the Chip supply shortage and
the US release of the Toniebox. Thats why we believe they just made some
adjustments to fit different electronic components because other might
not be available at that point of time, or Boxine had to do some
corrections for the US release.

Because the TI CC3200 was deprecated a while ago they had to come up
with the V3 wich implements the TI CC3235. The V3 Toniebox was released
at the beginning of 2022.

Besides of the PCB Layout and microcontroller changes the overall look
and user experience did not change in comparison of the three versions.

The downside (as of now) is, that our custom Bootloader and CFW does not
work yet with the V3. But we are working hard on this issue.

## **Final thoughts**

This is just a short introduction into hacking of the Toniebox. We
gained a lot more knowledge about how the Toniebox works and what are
the detailed processes behind the scenes…

If you think I should add more information about certain stuff, please
drop me a line at <gambrius@gmail.com> or leave a comment.

</div>

<span class="cat-links"><span class="screen-reader-text">Kategorien
</span>[Hardware Hacks](https://gt-blog.de/category/hardware-hacks/),
[Toniebox](https://gt-blog.de/category/toniebox/)</span>
<span class="tags-links"><span class="screen-reader-text">Schlagwörter
</span>[Boxine](https://gt-blog.de/tag/boxine/), [cointag](https://gt-blog.de/tag/coin-tag/), [customaudio](https://gt-blog.de/tag/custom-audio/), [customcontent](https://gt-blog.de/tag/custom-content/), [customtag](https://gt-blog.de/tag/custom-tag/),
[eBay](https://gt-blog.de/tag/ebay/),
[emulation](https://gt-blog.de/tag/emulation/),
[g3gg0](https://gt-blog.de/tag/g3gg0/),
[gambrius](https://gt-blog.de/tag/gambrius/),
[Hack](https://gt-blog.de/tag/hack/), [how
to](https://gt-blog.de/tag/how-to/),
[Klopfmethode](https://gt-blog.de/tag/klopfmethode/),
[knock](https://gt-blog.de/tag/knock/),
[methode](https://gt-blog.de/tag/methode/),
[NFC](https://gt-blog.de/tag/nfc/), [NXP](https://gt-blog.de/tag/nxp/),
[NXP manager](https://gt-blog.de/tag/nxp-manager/),
[own](https://gt-blog.de/tag/own/),
[RevvoX](https://gt-blog.de/tag/revvox/),
[RFID](https://gt-blog.de/tag/rfid/),
[RFIDfriend](https://gt-blog.de/tag/rfidfriend/),
[TagInfo](https://gt-blog.de/tag/taginfo/),
[Team](https://gt-blog.de/tag/team/),
[Tonie](https://gt-blog.de/tag/tonie/),
[Toniebox](https://gt-blog.de/tag/toniebox/)</span>


## Other work by the author

  - [Toniebox Hacking – How to get started](https://gt-blog.de/toniebox-hacking-how-to-get-started/)
  - [Gira 106 with Unifi Access NFC Reader](https://gt-blog.de/gira-106-with-unifi-access-nfc-reader/)
  - [Overview of the Children’s Audio Player Market – Q1/2021](https://gt-blog.de/overview-of-the-childrens-audio-player-market/)
  - [Teardown of the TECHNIFANT by TechniSat](https://gt-blog.de/teardown-of-the-technifant-by-technisat/)
  - [Firmware Update rolls out counter actions for custom tags](https://gt-blog.de/firmware-update-changes-behavior-with-custom-tags/)
