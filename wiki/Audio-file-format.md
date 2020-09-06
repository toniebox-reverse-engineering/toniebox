# SD card structure
Every box contains a SD card which is used to store the tonies audio data.

## downloaded audio files
The downloaded audio files for tonies are stored on the SD card in a directory for every tonie.

Directories are named by the last 4 bytes of the tonie ISO15693 UID in hex format, e.g. <SD>\DEADBEEF.
Within that folder there is a file named by the first 4 bytes of the UID.
Both hex values represent the tag's UID, but in reverse order.

So a tonie with the UID E00403500D0D3F47 has the audio content stored in the file <SD>\CONTENT\473F0D0D\500304E0.

## predefined files
Upon initalization the box extracts the content of the flash-internal sfx.bin into two directories with several audio files:

    00000000\000000*
    00000001\000000*

# Audio file format
In general the audio files are just OGG files with some custom header

So the files are structured like this:

    <file>   ::= <header> <audio_data>
    <header> ::= <header_len> <header_data>
    
    where:
    <header_len>  length of <header_data> in big endian uint32, usually 0x00000FFC
    <header_data> protobuf coded info fields like SHA1 hash, audio length, etc
    <audio_data>  Ogg audio file

# Header format

The file header is coded using protobuf and contains these fields:

    1. [string]   Audio data SHA-1 hash
    2. [variant]  Audio data length in bytes
    3. [variant]  Audio-ID of OGG audio file, which is the unix time stamp of file creation
    4. [string]   [array of variant] Ogg page numbers for Chapters
    5. [string]   fill bytes „00“ up to <header_len>
   
To decode the protobuf content, you can use the online decoder at https://protogen.marcgravell.com/decode

Encoding is a bit more tricky, as the tested encoder did not produce the correct data for the 4th field.
Here the protobuf field type should be "string" and the content should be an array of multiple variants.
One variant coded page number for every chapter in the file, starting with a zero for the first chapter.

The encoder produced either multiple variant fields with the same field number, or the correct string field
except for files with only one chapter where it generated only a variant field.
Long story short, the best choice was to build a custom protobuf encoder.

# Audio data

The container format for the audio data is Ogg, which packetizes the data into so called "pages".
Pages contain metadata like the time granule (timestamp) for playback, sequence number, checksum etc. and
the real audio data in segments within the page.
See https://en.wikipedia.org/wiki/Ogg_page

The tonie files are encoded using an opus coder with around 96-116 kbps in VBR mode. (opus header say 96 kbps)
The encoder was set up to produce Ogg pages that perfectly fit into a 4k (0x1000) byte sized page.
As the box seems to read the data from SD into a 4k byte sized buffer, pages are only
allowed to start at 4k-boundaries and must end at the end of the page. Pages can not cross the 4k boundary, 
else the file is treaten as invalid and gets re-downloaded.

There is no (to me known) way of "padding" data in a page so that the box would accept the data as valid.
Thus the encoder must be configured in CBR mode with a certain bit rate, such that Ogg page header plus segments
build up 4k sized blocks starting at 4k-offsets and ending at 4k-offsets.
For sure there is a way to tell the opus coder "now please produce a segment with n bytes" which can be
used to fill up the page until it's 4k end.
But the in experiments used encoder did not have an obvious feature to do this.

**We have developed a tool called [teddy](https://github.com/toniebox-reverse-engineering/teddy) to encode and decode these files.**

