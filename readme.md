# This my hobby make some web to flash my firmware
# Firmware support for board 
# Model
- ESP32-1732S019 (320x170) 1.9inch.
# Cheap Yellow Display (CYD) ESP32 Development Boards

![Streaming Demo](./image/ESP32-1732S019.avif)

## Upload firmware [ESP-Tool Click Here!!👈🏻](https://binarybearzz.github.io/esp-tool-s3screenmirror/)
![Streaming Demo](./image/web-esp-tool.png)

## Download [ScreenCaptureTool(Build exe)👇🏻](https://binarybearzz.github.io/esp-tool-s3screenmirror/tools/esp32-streammirrorcapture-continue.exe)

![Streaming Demo](./image/streammirrorcapture.png)

## Source code [ScreenCaptureTool👈🏻](https://github.com/BinaryBearzz/esp-tool-s3screenmirror/tree/main/tools/esp32-streammirrorcapture-continue.py)
<br>

```mermaid
flowchart TD
    PC["PC with Python App<br/>(Screen Capture & JPEG Compression)"]
    ESP32["ESP32 Device<br/>(WiFi + TCP Server + JPEG Decoder + TFT)"]

    PC -->|1. Capture selected monitor screen| PC
    PC -->|2. JPEG compress captured frame| PC
    PC -->|3. Establish TCP connection| ESP32
    PC -->|4. Send 4-byte frame size| ESP32
    PC -->|5. Send JPEG frame data| ESP32
    ESP32 -->|6. Decode JPEG and render on TFT| ESP32
    PC -->|7. Repeat at interval ~50 ms| PC

    subgraph Streaming_Process
        PC
        ESP32
    end


- This web flasher is powered by [ESP Web Tools](https://github.com/esphome/esp-web-tools), a project by the [ESPHome](https://github.com/esphome) team.

- ESP Web Tools uses [esptool.js](https://github.com/esphome/esp-web-tools/tree/main/esptool-js) under the hood to flash firmware directly from your browser to ESP32 and ESP8266 devices.

- [Improve-WiFi](https://www.improv-wifi.com/serial) config WiFi via Serial.

## Authors

- [@BinaryBearx](https://github.com/BinaryBearzz)
