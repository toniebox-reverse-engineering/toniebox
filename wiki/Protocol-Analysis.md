# prod.de.tbs.toys
## Basics
The communication is based on HTTPS (TLS over HTTP). The box authenticates with a client certificate (private.der/client.der) to the server. The cc3200 based boxed may use an outdated sha1 based algorithm that may lead to problems with modern OpenSSL versions.

### Request
Every request contains a user-agent header with information about the current running firmware and the box' hardware.
There may be additional headers such as a content-length or authoritation if needed.

#### Example
| Variable | Description | Example |
|---|---|---|
| sp | 8-digit-number |  |
| hw | 7-digit-number |  |
| firmware-ts | unix-timestamp | 1640950635 |
| box-color | Box' color (only esp32) | RoseRed |
##### cc3200
    GET https://prod.de.tbs.toys/%path% HTTP/1.1
    Host: prod.de.tbs.toys
    User-Agent: TB/%firmware-ts% SP/%sp% HW/%hw%
##### cc3235
    GET https://prod.de.tbs.toys/%path% HTTP/1.1
    Host: prod.de.tbs.toys
    User-Agent: TB/%firmware-ts% SP/%sp% HW/%hw%
##### esp32
    GET https://prod.de.tbs.toys/%path% HTTP/1.1
    Host: prod.de.tbs.toys
    User-Agent: %box-color% TB/%firmware-ts%

### Response
| Variable | Description | Example |
|---|---|---|
| http-code | http standard code | 200 OK |
| request-id | 20-alphanumeric id |  Ff2n6tTjF-fJz5Ai-2Ts |
| content-len | integer for the content length | 0 |

#### Example
    HTTP/1.1 %http-code%
    Server: openresty
    Date: Mon, 30 Jan 2023 17:40:04 GMT
    Content-Length: %content-len%
    Connection: keep-alive
    cache-control: max-age=0, private, must-revalidate
    x-request-id: %request-id%

## Endpoints
### v1-time (GET /v1/time) 
Receive the time in unix time format. May be needed for the TLS-certificates. 

#### Response-Headers
| Header | Description | Example |
|---|---|---|
| Content-Length | integer | 10 |
| Content-Type | | text/plain; charset=utf-8 |
#### Response
    1675100403
#### This value would correspond to 
    Mon Jan 30 2023 17:40:03 GMT+0000

### v1-ota (GET /v1/ota/%file-id%?cv=%file-ts%)
Updates several files within the box.

Responses with HTTP 304 Not Modified if file is already up to date otherwise with the content of the file and a HTTP 200 OK.

#### Variables
| Variable | Description | Example |
|---|---|---|
| file-id | one-digit number (2-6)| 3 |
| file-ts | unix-timestamp of the  | 1640950635 |
#### Files
| File ID | Name | Description |
|---|---|---|
| 2 | PD-Firmware | |
| 3 | EU-Firmware | |
| 4 | Service Pack (cc3200) | |
| 5 | HTML | |
| 6 | SFX | |

### v1-freshness-check (POST /v1/freshness-check)
Sends all Audio-IDs and UIDs of the content on box to the cloud in protobof. The result contains the UIDs of the files that should be marked hidden. In addition several settings (volume / skipping)

#### Request-Headers
| Header | Description | Example |
|---|---|---|
| Content-Length | integer | 400 |
#### Request-Protobuf
    message TonieFreshnessCheckRequest {
    repeated TonieFCInfo tonie_infos = 1;
    }

    message TonieFCInfo {
    required fixed64 uid = 1;
    required fixed32 audio_id = 2;
    }
#### Response-Headers
| Header | Description | Example |
|---|---|---|
| Content-Length | integer | 23 |
| Content-Type | | application/octet-stream; charset=utf-8 |
#### Response-Protobuf
    message TonieFreshnessCheckResponse {
    repeated fixed64 tonie_marked = 1;
    required int32 field2 = 2;
    required int32 max_vol_spk = 3; #0-3
    required int32 slap_en = 4; #1=on, 0=off
    required int32 slap_dir = 5; #1=back-left_forw-right, 0=forw-left_back-right
    required int32 field6 = 6;
    required int32 max_vol_hdp = 7; #0-3
    required int32 led = 8; #0=on, 1=off, 2=dimmed
    }

### v2-content (GET /v2/content/%uid-rev%)
Gets the content by uid and a password. If the content is know it sent back via HTTP 200 OK. The box may try to get a partial file. Then the answer is a HTTP 206 Partial Content (TODO).

#### Variables 
| Variable | Description | Example |
|---|---|---|
| uid-rev | 8-Byte UID reversed | 3e3a1aa3500304e0 |
| content-pass | Memory-content of the tag (32-byte hex) | 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef |
#### Request-Headers
| Header | Description | Example |
|---|---|---|
| Authorization | Contains the "password" for the content to download | BD: %content-pass% |
#### Response-Headers
| Header | Description | Example |
|---|---|---|
| Content-Length | integer | 23232 |
| Content-Type | | binary/octet-stream |

### v1-claim (GET /v1/claim/%uid-rev%)

#### Variables 
| Variable | Description | Example |
|---|---|---|
| uid-rev | 8-Byte UID reversed | 3e3a1aa3500304e0 |
| content-pass | Memory-content of the tag (32-byte hex) | 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef |
#### Request-Headers
| Header | Description | Example |
|---|---|---|
| Authorization | Contains the "password" for the content | BD %content-pass% |
#### Response-Headers
| Header | Description | Example |
|---|---|---|
| Content-Length | integer | 0 |

# rtnl.bxcl.de
## Basics
The communication is based on a TLS stream and **protobuf** and is unidirectional towards boxine. It's (nearly) identical to the output via UART. 
## Tool
[RTNL Decoder](https://github.com/toniebox-reverse-engineering/toniebox/blob/master/tools/rtnl_decoder.py)
## Bytes
### AP SSID
### SD Directory
### Firmware version / Update
### MAC
