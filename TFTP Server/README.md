# TFTP (Trivial File Transfer Protocol)

簡單檔案傳輸協定<br/>
RFC 1350<br/>
Layer 7 protocal<br/>
Layer 4: UDP（所以不用 handshaking）<br/>
TFTP Server: UDP port 69<br/>

## Messages

<br/>

| Operation Code | Message |
| --- | --- |
| 01 | **RRQ (Read Request)** <br/>- 從 server 下載檔案<br/>|
| 02 | **WRQ (Write Request)** <br/>- 上傳檔案至 server<br/>|
| 03 | **DATA** <br/>- 傳送檔案資料，上傳和下載格式都一樣<br/> |
| 04 | **ACK** <br/>- acknowledgement<br/>|
| 05 | **ERROR** <br/>- 回報傳輸錯誤<br/>|
<br/>
RRQ 和 WRQ 格式相同<br/>
每個 message 的前 2 個 bytes 會記載這個 message 的種類（operation code）<br/>

<br/>

>Details
<br/>
>https://github.com/angel870326/Socket_Programming/blob/main/TFTP%20Server/TFTP_intro_note.pdf
<br/>
>Source: https://youtu.be/N9f3WQhf1vQ
