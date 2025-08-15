# Communication Design Project 🚀  

## Overview  
This project involves the design and implementation of transceivers for communication systems using various modulation, encoding, and encryption techniques. Each transceiver setup is built with unique features to enhance reliability, performance, and security. The transceivers are implemented using Software-Defined Radios (SDR), GNU Radio, and BladeRF hardware.  

For flexibility, the project supports both:  
- **Hardware Mode (BladeRF)** – real SDR transmission and reception  
- **Local Simulation Mode** – for testing the transceiver logic without BladeRF hardware  
  - With AES encryption enabled (`app_local_aes.py`)  
  - Without encryption (`app_local.py`)  

---

## Features  
- **QPSK (Quadrature Phase Shift Keying)** – High data rate transceiver for robust communication.  
- **QPSK with FEC (Forward Error Correction)** – Enhanced reliability by correcting errors without retransmission.  
- **QPSK with CRC (Cyclic Redundancy Check)** – Detect and verify errors for increased accuracy.  
- **GMSK (Gaussian Minimum Shift Keying)** – Efficient bandwidth modulation for optimal signal performance.  
- **AES Encryption & Decryption** – Secures transmitted data in AES-enabled modes.  

---

## How It Works  
### AES-enabled Local Simulation Mode Data Flow
```
        ┌────────────┐
        │ Input File │
        └─────┬──────┘
              │
       AES Encryption (CBC)
              │
              ▼
        ┌──────────────┐
        │ Cipher File  │
        └─────┬────────┘
              │
     Add Preamble + CRC
              │
              ▼
        ┌──────────────┐
        │   TMP File   │
        └─────┬────────┘
              │
           (Transmit in Hardware mode)
              │
              ▼
        ┌──────────────┐
        │   TMP File   │
        └─────┬────────┘
              │
  Remove Preamble + CRC Check
              │
              ▼
       AES Decryption (CBC)
              │
              ▼
        ┌────────────┐
        │ Output File│
        └────────────┘
```

---

## Technologies Used  
- **Software:**  
  - GNU Radio – Signal processing and SDR integration  
  - MATLAB – Simulation and algorithm prototyping  
  - Python – Data processing and control scripts  
  - PyCryptodome – AES encryption/decryption  
  - Streamlit – GUI application framework  

- **Hardware:**  
  - BladeRF SDR – For live signal transmission and reception  
  - SDR Framework – Flexible modulation scheme implementation  

---

## Modes of Operation  

| Mode | Script | Encryption | Requires BladeRF? |
|------|--------|-----------|--------------------|
| **Hardware** | `app.py` | Optional (AES integrated) | ✅ Yes |
| **Local (AES)** | `app_local_aes.py` | ✅ Enabled | ❌ No |
| **Local (No AES)** | `app_local.py` | ❌ Disabled | ❌ No |

---

## Prerequisites  
1. Install Python 3.12 or newer.  
2. Install required packages:  
   ```bash
   pip install streamlit pycryptodome
   ```
3. Ensure the following scripts are in your working folder:  
   - `app.py` (hardware mode)  
   - `app_local_aes.py` (local AES simulation)  
   - `app_local.py` (local simulation without AES)  
   - `addPreamble.py`  
   - `aes_encryptor.py`  
   - `aes_decryptor.py`  
   - `crctransmitter.py`  
   - `crcreceiver.py`  
   - `removePreamble.py`  

---

## Running the Apps  

### **1. Hardware Mode (BladeRF)**  
```bash
streamlit run app.py
```
- Choose **Backend → Hardware (BladeRF scripts)** in the sidebar.  
- Follow the transmitter/receiver steps below.  

---

### **2. Local Simulation Mode – AES Enabled**  
```bash
streamlit run app_local_aes.py
```
- Choose **Backend → Simulated (No-RF)** in the sidebar.  
- AES encryption is always ON.  
- Provide:
  - **Input file path** (plaintext)
  - **TMP file path** (intermediate file after preamble and CRC)
  - **Key file path** (will be created at TX, must be reused at RX)
- On RX:
  - Use the same TMP file from TX.
  - Use the same Key file from TX.
  - The final output will be the decrypted original file.

---

### **3. Local Simulation Mode – No AES**  
```bash
streamlit run app_local.py
```
- Choose **Backend → Simulated (No-RF)** in the sidebar.  
- Encryption is OFF.  
- Just provide:
  - **Input file** → TMP file after preamble and CRC → Output file after preamble removal.  

---

## Transmitter Steps (All Modes)  
1. Enter **input file path** (plaintext in AES mode).  
2. Enter **TMP output path** (file after preamble; `.tmp` or `.bin` suggested).  
3. If AES is enabled:
   - Provide a **Key file path** (e.g., `secret.key`).
4. Set **Samples per symbol** and **Multiply constant** as required.  
5. Click **🦜 Start Transmitting**.

---

## Receiver Steps (All Modes)  
1. Enter **TMP file path** (same as TX output).  
2. If AES is enabled:
   - Provide the **Key file path** (same as TX used).  
3. Enter **final output file path** (where plaintext will be saved).  
4. Click **📥 Start Receiving**.

---

## Troubleshooting  
- **`No module named 'Crypto'`** → Install PyCryptodome:
  ```bash
  pip install pycryptodome
  ```
- Ensure file paths exist and are correct.  
- Keep the `secret.key` file safe — you need it for decryption.  
- If using Hardware mode, make sure BladeRF drivers are installed and device is connected.  
- For local simulation, no SDR hardware is required.  

---
