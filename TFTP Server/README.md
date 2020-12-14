# TFTP (Trivial File Transfer Protocol)

簡單檔案傳輸協定<br/>
RFC 1350<br/>
Layer 7 protocal<br/>
Layer 4: UDP<br/>
TFTP Server: UDP port 69<br/>

## Messages

<br/>

| Operation Code | Message |
| --- | --- |
| 01 | **RRQ (Read Request)** <br/>- 從 server 下載檔案<br/>|
| 02 | **WRQ (Write Request)** <br/>- 上傳檔案至 server<br/>|
| 03 | - |
| 04 | - |
| 05 | - |
<br/>
RRQ 和 WRQ 格式相同


