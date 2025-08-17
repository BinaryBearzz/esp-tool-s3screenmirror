# This my hobby make some thing cool this web for flash firmware my project
# Firmware support for board ( 2 model )
# ⚡Model
# 1. ESP32-1732S019 (320x170) 1.9inch.
# Cheap Yellow Display (CYD) ESP32 Development Boards

![Streaming Demo](./image/ESP32-1732S019.avif)


# 2. ESP32-2432S028R (320x240) 1.9inch.
# Cheap Yellow Display (CYD) ESP32 Development Boards

![Streaming Demo](./image/ESP32-2432S028R.webp)


## 🔨 Upload firmware [ESP-Tool Click Here!!👈🏻](https://binarybearzz.github.io/esp-tool-s3screenmirror/)
![Streaming Demo](./image/web-esp-tool.png)

## ⬇️ Download [ScreenCaptureTool(Build exe)👇🏻](https://raw.githubusercontent.com/BinaryBearzz/esp-tool-s3screenmirror/refs/heads/main/tools/esp32-streammirrorcapture-continue.exe)

![Streaming Demo](./image/streammirrorcapture.png)

## 📄 Source code [ScreenCaptureTool👈🏻](https://github.com/BinaryBearzz/esp-tool-s3screenmirror/tree/main/tools/esp32-streammirrorcapture-continue.py)
<br>

```mermaid
flowchart TD
    PC["PC with Python App Screen Capture & JPEG Compression"]
    ESP32["ESP32 Device (WiFi + TCP Server + JPEG Decoder + TFT)"]

    PC -->| Capture selected monitor screen| PC
    PC -->| JPEG compress captured frame| PC
    PC -->|1.Establish TCP connection| ESP32
    PC -->|2.Send 4-byte frame size| ESP32
    PC -->|3.Send JPEG frame data| ESP32
    ESP32 -->|4.Decode JPEG and render on TFT| ESP32
    PC -->|Interval Repeat every 50 ms| PC

    subgraph Streaming Process
        PC
        ESP32
    end

```

- This web flasher is powered by [ESP Web Tools](https://github.com/esphome/esp-web-tools), a project by the [ESPHome](https://github.com/esphome) team.

- ESP Web Tools uses [esptool.js](https://github.com/esphome/esp-web-tools/tree/main/esptool-js) under the hood to flash firmware directly from your browser to ESP32 and ESP8266 devices.

- [Improve-WiFi](https://www.improv-wifi.com/serial) config WiFi via Serial.

## Authors

- [@BinaryBearx](https://github.com/BinaryBearzz)
