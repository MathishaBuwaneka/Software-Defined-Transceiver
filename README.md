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

## Operating the QPSK CRC Transceiver Application  

Download the folder named **'appCRCTranceiver QPSK'** which includes all required Python files.  

### Prerequisites  
1. Ensure you have **Python** installed on your system.  
2. Install **Streamlit** and other required Python packages using:  
   ```bash  
   pip install streamlit  
   ```  
3. Verify that the following Python scripts are present in the downloaded folder:  
   - `app.py`
   - `addPreamble.py`  
   - `crctransmitter.py`  
   - `crcreceiver.py`  
   - `removePreamble.py`
     

### Steps to Operate the App  

1. **Start the App:**  
   - Open a terminal or command prompt.  
   - Run the Streamlit app using:  
     ```bash  
     streamlit run app.py  
     ```  

2. **Choose Operation:**  
   - Use the **sidebar** to select either the **Transmitter** or **Receiver** page.  

#### Transmitter Instructions  
1. Enter the file path of the **input file** under **Enter file location** (e.g., `C:\path\to\file.txt`).  
2. Enter the **output path** where the temporary file should be saved(Tmp file which was created after appending the preamble.E.g., `C:\path\to\file.tmp`).  
3. Adjust:  
   - **Samples per symbol** (default: 2).  
   - **Multiply constant** (default: 0.707).  
4. Click **🦜 Start Transmitting** to begin:  
   - The app processes the input file with `addPreamble.py`.  
   - It then transmits using `crctransmitter.py`.  
5. Observe the success or error messages for each step.  

**Note:** Ensure the BladeRF device is connected before starting transmission.  

#### Receiver Instructions  
1. Enter the **destination path** for the received file(e.g., `C:\path\to\file.txt`).  
2. Specify the **temporary file path** for saving intermediate data(Location to save the received Tmp file.E.g., `C:\path\to\file.tmp`).  
3. Adjust:  
   - **Samples per symbol** (default: 2).  
   - **Multiply constant** (default: 0.707).  
4. Click **📥 Start Receiving** to begin:  
   - The app receives the file with `crcreceiver.py`.  
   - It processes the received file with `removePreamble.py`.  
5. Check the success or error messages displayed for each step.  

**Note:** Ensure the BladeRF device is connected before starting reception.  

### Troubleshooting  
- If the app fails, ensure all paths and file extentions are correct.

