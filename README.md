# Communication Design Project 🚀  

## Overview  
This project involves the design and implementation of transceivers for communication systems using various modulation and encoding techniques. Each transceiver setup is built with unique features to enhance reliability and performance. The transceivers are implemented using **Software-Defined Radios (SDR)**, **GNU Radio**, and **BladeRF** hardware.  

### Features  
- **QPSK (Quadrature Phase Shift Keying):** High data rate transceiver for robust communication.  
- **QPSK with FEC (Forward Error Correction):** Enhanced reliability by correcting errors without retransmission.  
- **QPSK with CRC (Cyclic Redundancy Check):** Detect and verify errors for increased accuracy.  
- **GMSK (Gaussian Minimum Shift Keying):** Efficient bandwidth modulation for optimal signal performance.  

## How It Works  
1. **QPSK Transceiver:**  
   - Modulates digital data into QPSK signals and demodulates it back at the receiver.  
2. **QPSK with FEC:**  
   - Implements error correction coding at the transmitter and decoding at the receiver for reliable communication.  
3. **QPSK with CRC:**  
   - Adds a CRC code at the transmitter for error detection and verifies data integrity at the receiver.  
4. **GMSK Transceiver:**  
   - Uses Gaussian filtering to smooth frequency transitions, ensuring bandwidth efficiency.  

## Technologies Used  
- **Software:**  
  - GNU Radio: Signal processing and SDR integration  
  - MATLAB: Simulation and algorithm prototyping  
  - Python: Data processing and control scripts  
- **Hardware:**  
  - BladeRF SDR: For signal transmission and reception  
  - SDR Framework: Ensuring flexibility in implementing modulation schemes  


