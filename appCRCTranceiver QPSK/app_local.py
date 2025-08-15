import streamlit as st
import subprocess
import zlib
from pathlib import Path

# -----------------------------
# Helpers for simulation
# -----------------------------
PREAMBLE = b"PREAMBLE::QPSK::"

def _norm(path_str: str) -> Path:
    # Expand ~, normalize slashes, and return a Path
    return Path(Path(path_str).expanduser())

def simulate_add_preamble(input_path: str, output_path: str) -> str:
    ip = _norm(input_path)
    op = _norm(output_path)
    data = ip.read_bytes()
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_bytes(PREAMBLE + data)
    return f"Added preamble ({len(PREAMBLE)} bytes). Input={ip}, Output={op}, Size={op.stat().st_size} bytes"

def simulate_crc_transmit(file_path: str, sps: int, mult: float) -> str:
    fp = _norm(file_path)
    data = fp.read_bytes()
    crc = zlib.crc32(data) & 0xFFFFFFFF
    with fp.open("ab") as f:
        f.write(crc.to_bytes(4, "big"))
    return (
        "Sim TX complete.\n"
        f"- SPS={sps}, Mult={mult}\n"
        f"- CRC32 appended=0x{crc:08X}\n"
        f"- File={fp}, NewSize={fp.stat().st_size} bytes"
    )

def simulate_crc_receive(file_path: str, sps: int, mult: float) -> str:
    fp = _norm(file_path)
    # In simulation we just report; in a real RX you’d write to fp
    size = fp.stat().st_size if fp.exists() else 0
    return (
        "Sim RX complete.\n"
        f"- SPS={sps}, Mult={mult}\n"
        f"- File={fp}, Size={size} bytes"
    )

def simulate_remove_preamble(input_path: str, output_path: str) -> str:
    ip = _norm(input_path)
    op = _norm(output_path)
    blob = ip.read_bytes()
    if len(blob) < len(PREAMBLE) + 4:
        raise ValueError("File too small to contain preamble and CRC.")

    # Separate CRC (last 4 bytes)
    data_wo_crc = blob[:-4]
    given_crc = int.from_bytes(blob[-4:], "big")

    # Check and strip preamble
    if not data_wo_crc.startswith(PREAMBLE):
        raise ValueError("Preamble not found — file did not start with expected prefix.")

    payload = data_wo_crc[len(PREAMBLE):]
    calc_crc = zlib.crc32(data_wo_crc) & 0xFFFFFFFF  # CRC was computed on data incl. preamble during TX

    # For integrity, we typically want CRC over payload only; but since TX appended CRC of the entire
    # data at that time (preamble+payload), we verify against that.
    if calc_crc != given_crc:
        raise ValueError(f"CRC mismatch: expected 0x{given_crc:08X}, got 0x{calc_crc:08X}")

    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_bytes(payload)
    return (
        "Preamble removed and CRC verified.\n"
        f"- Input={ip}\n- Output={op}\n- PayloadSize={len(payload)} bytes\n"
        f"- CRC OK=0x{given_crc:08X}"
    )

# -----------------------------
# UI Pages
# -----------------------------

def transmitter_page(mode: str):
    st.title("🚀 **Transmitter**")
    st.markdown("<hr style='border:1px solid #f63366;'>", unsafe_allow_html=True)

    # File location input
    file_location1 = st.text_input("📂 **Enter input file path:**", help=r"e.g. C:\Users\You\Desktop\gui.tx")
    file_location2 = st.text_input("📄 **Enter path to save TMP (tx intermediate):**")

    # Additional inputs
    samples_per_symbol = st.number_input("**Samples per symbol (SPS):**", min_value=1, value=2)
    multiply_constant = st.number_input("**Multiply constant:**", value=0.707, format="%.3f")

    # Start transmitting button
    if st.button("🦜 **Start Transmitting**"):
        if not file_location1 or not file_location2:
            st.error("⚠️ Please provide both input and TMP output paths.")
            return

        try:
            if mode == "Simulated (No-RF)":
                # Step 1: add preamble
                out1 = simulate_add_preamble(file_location1, file_location2)
                st.success(f"TMP saved to **{file_location2}**")
                st.code(out1)

                # Step 2: append CRC and 'transmit'
                out2 = simulate_crc_transmit(file_location2, samples_per_symbol, multiply_constant)
                st.success("Transmission (simulated) complete!")
                st.code(out2)

            else:
                # Hardware mode (use your existing scripts)
                command1 = [
                    "python", "addPreamble.py",
                    "--input_path_tx", file_location1,
                    "--output_path_tx", file_location2
                ]
                result1 = subprocess.run(command1, text=True, capture_output=True)
                if result1.returncode == 0:
                    st.success(f"TMP saved to **{file_location2}**")
                    st.code(result1.stdout or "(no output)")
                    command2 = [
                        "python", "crctransmitter.py",
                        "--filename-variable", file_location2,
                        "--spss", str(samples_per_symbol),
                        "--multiplyconn", str(multiply_constant)
                    ]
                    result2 = subprocess.run(command2, text=True, capture_output=True)
                    if result2.returncode == 0:
                        st.success("Transmission successfully!")
                        st.code(result2.stdout or "(no output)")
                    else:
                        st.error("⚠️ Error during transmission script.")
                        st.code(result2.stderr)
                else:
                    st.error("⚠️ Error while adding preamble.")
                    st.code(result1.stderr)

        except Exception as e:
            st.error(f"⚠️ Failed: {e}")

    st.markdown("<p style='color:gray; font-size:12px;'>In Hardware mode, ensure the BladeRF is connected.</p>", unsafe_allow_html=True)

def receiver_page(mode: str):
    st.title("📡 **Receiver**")
    st.markdown("<hr style='border:1px solid #2c75c1;'>", unsafe_allow_html=True)

    # File destination address input
    file_destination2 = st.text_input("🏠 **Final output file path (decoded):**")
    file_destination1 = st.text_input("📄 **TMP path to save received (rx intermediate):**", help=r"e.g. C:\Users\You\Desktop\gui.txt")

    # Additional inputs
    samples_per_symbol = st.number_input("**Samples per symbol (SPS):**", min_value=1, value=2, key="rx_sps")
    multiply_constant = st.number_input("**Multiply constant:**", value=0.707, format="%.3f", key="rx_mult")

    # Start receiving button
    if st.button("📥 **Start Receiving**"):
        if not file_destination1 or not file_destination2:
            st.error("⚠️ Please provide both RX TMP and final output paths.")
            return

        try:
            if mode == "Simulated (No-RF)":
                # Step 1: "receive" (no change to file; assume TX TMP already exists)
                out1 = simulate_crc_receive(file_destination1, samples_per_symbol, multiply_constant)
                st.success(f"Received TMP at **{file_destination1}**")
                st.code(out1)

                # Step 2: remove preamble and verify CRC → write final
                out2 = simulate_remove_preamble(file_destination1, file_destination2)
                st.success("Preamble removed (simulated) and CRC verified!")
                st.code(out2)

            else:
                # Hardware mode (use your existing scripts)
                command1 = [
                    "python", "crcreceiver.py",
                    "--recfilename-variable", file_destination1,
                    "--spss", str(samples_per_symbol),
                    "--multiplyconn", str(multiply_constant)
                ]
                result1 = subprocess.run(command1, text=True, capture_output=True)
                if result1.returncode == 0:
                    st.success(f"Saved received TMP to **{file_destination1}**!")
                    st.code(result1.stdout or "(no output)")

                    command2 = [
                        "python", "removePreamble.py",
                        "--input_path_rx", file_destination1,
                        "--output_path", file_destination2
                    ]
                    result2 = subprocess.run(command2, text=True, capture_output=True)
                    if result2.returncode == 0:
                        st.success("Removing preamble successful!")
                        st.code(result2.stdout or "(no output)")
                    else:
                        st.error("⚠️ Error occurred while removing the preamble.")
                        st.code(result2.stderr)
                else:
                    st.error("⚠️ Error occurred while receiving TMP file.")
                    st.code(result1.stderr)

        except Exception as e:
            st.error(f"⚠️ Failed: {e}")

    st.markdown("<p style='color:gray; font-size:12px;'>In Hardware mode, ensure the BladeRF is connected.</p>", unsafe_allow_html=True)

# -----------------------------
# Main
# -----------------------------
def main():
    st.sidebar.title("QPSK Transceiver")
    mode = st.sidebar.selectbox("Backend", ["Simulated (No-RF)", "Hardware (BladeRF scripts)"])
    page = st.sidebar.radio("Choose:", ["🡵 Transmitter", "🡷 Receiver"])

    if page == "🡵 Transmitter":
        transmitter_page(mode)
    else:
        receiver_page(mode)

if __name__ == "__main__":
    main()
