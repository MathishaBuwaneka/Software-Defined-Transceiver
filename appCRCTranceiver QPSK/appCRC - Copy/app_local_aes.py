import streamlit as st
import subprocess
import zlib
from pathlib import Path

# -----------------------------
# Config & helpers
# -----------------------------
PREAMBLE = b"PREAMBLE::QPSK::"

def _p(path_str: str) -> Path:
    return Path(path_str).expanduser()

def _default_with_suffix(path_str: str, suffix: str) -> Path:
    p = _p(path_str)
    return p.with_suffix(p.suffix + suffix)

# ---- Simulation helpers (no-RF) ----
def simulate_add_preamble(input_path: str, output_path: str) -> str:
    ip, op = _p(input_path), _p(output_path)
    data = ip.read_bytes()
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_bytes(PREAMBLE + data)
    return f"Added preamble ({len(PREAMBLE)} bytes). Input={ip}, Output={op}, Size={op.stat().st_size} bytes"

def simulate_crc_append(file_path: str, sps: int, mult: float) -> str:
    fp = _p(file_path)
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
    fp = _p(file_path)
    size = fp.stat().st_size if fp.exists() else 0
    return (
        "Sim RX complete.\n"
        f"- SPS={sps}, Mult={mult}\n"
        f"- File={fp}, Size={size} bytes"
    )

def simulate_remove_preamble_and_check_crc(input_path: str, output_path: str) -> str:
    ip, op = _p(input_path), _p(output_path)
    blob = ip.read_bytes()
    if len(blob) < len(PREAMBLE) + 4:
        raise ValueError("File too small to contain preamble and CRC.")
    data_wo_crc = blob[:-4]
    given_crc = int.from_bytes(blob[-4:], "big")

    if not data_wo_crc.startswith(PREAMBLE):
        raise ValueError("Preamble not found at start of file.")
    calc_crc = zlib.crc32(data_wo_crc) & 0xFFFFFFFF
    if calc_crc != given_crc:
        raise ValueError(f"CRC mismatch: expected 0x{given_crc:08X}, got 0x{calc_crc:08X}")

    payload = data_wo_crc[len(PREAMBLE):]
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_bytes(payload)
    return (
        "Preamble removed and CRC verified.\n"
        f"- Input={ip}\n- Output={op}\n- PayloadSize={len(payload)} bytes\n"
        f"- CRC OK=0x{given_crc:08X}"
    )

# ---- AES helpers (via your scripts) ----
def aes_encrypt(infile: str, outfile: str, keyfile: str) -> str:
    cmd = [
        "python", "aes_encryptor.py",
        "--infile", str(_p(infile)),
        "--outfile", str(_p(outfile)),
        "--keyfile", str(_p(keyfile)),
    ]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"AES encrypt failed:\n{res.stderr}")
    return res.stdout or "AES encryption done."

def aes_decrypt(infile: str, outfile: str, keyfile: str) -> str:
    cmd = [
        "python", "aes_decryptor.py",
        "--infile", str(_p(infile)),
        "--outfile", str(_p(outfile)),
        "--keyfile", str(_p(keyfile)),
    ]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"AES decrypt failed:\n{res.stderr}")
    return res.stdout or "AES decryption done."

# -----------------------------
# UI Pages
# -----------------------------
def transmitter_page(mode: str, use_aes: bool, key_path: str):
    st.title("🚀 **Transmitter**")
    st.markdown("<hr style='border:1px solid #f63366;'>", unsafe_allow_html=True)

    in_file = st.text_input("📂 **Input file (plaintext if AES enabled):**", help=r"e.g. C:\Users\You\Desktop\input.bin")
    tx_tmp = st.text_input("📄 **TX TMP (after preamble [+CRC in Sim]):**", help=r"e.g. C:\Users\You\Desktop\tmp_tx.bin")
    enc_tmp = st.text_input("🔒 (Optional) Encrypted intermediate path", help="Leave empty to auto-derive")
    sps = st.number_input("**Samples per symbol (SPS):**", min_value=1, value=2)
    mult = st.number_input("**Multiply constant:**", value=0.707, format="%.3f")

    if st.button("🦜 **Start Transmitting**"):
        try:
            if not in_file or not tx_tmp:
                st.error("Please provide both Input file and TX TMP path.")
                return

            # Derive encrypted path if AES is on and not given
            if use_aes:
                if not key_path:
                    st.error("AES is enabled — please provide a Key file path in the sidebar.")
                    return
                enc_path = enc_tmp.strip() or str(_default_with_suffix(tx_tmp, ".enc"))
                # 1) Encrypt plaintext -> enc_path
                out = aes_encrypt(in_file, enc_path, key_path)
                st.success("AES encryption complete.")
                st.code(out)
                # 2) Add preamble on ciphertext -> tx_tmp
                out = simulate_add_preamble(enc_path, tx_tmp) if mode == "Simulated (No-RF)" else run_add_preamble(enc_path, tx_tmp)
                st.success(f"Preamble added → {tx_tmp}")
                st.code(out)
            else:
                # No AES: add preamble directly on plaintext
                out = simulate_add_preamble(in_file, tx_tmp) if mode == "Simulated (No-RF)" else run_add_preamble(in_file, tx_tmp)
                st.success(f"Preamble added → {tx_tmp}")
                st.code(out)

            # 3) Transmit
            if mode == "Simulated (No-RF)":
                out = simulate_crc_append(tx_tmp, sps, mult)
                st.success("Transmission (simulated) complete!")
                st.code(out)
            else:
                out = run_hw_tx(tx_tmp, sps, mult)
                st.success("Transmission (hardware) complete!")
                st.code(out)

        except Exception as e:
            st.error(f"⚠️ TX failed: {e}")

    st.markdown("<p style='color:gray; font-size:12px;'>Hardware mode uses your BladeRF scripts. Sim mode uses local files only.</p>", unsafe_allow_html=True)

def receiver_page(mode: str, use_aes: bool, key_path: str):
    st.title("📡 **Receiver**")
    st.markdown("<hr style='border:1px solid #2c75c1;'>", unsafe_allow_html=True)

    rx_tmp = st.text_input("📄 **RX TMP (received with preamble [+CRC in Sim]):**", help=r"e.g. C:\Users\You\Desktop\tmp_rx.bin")
    cip_out = st.text_input("🔐 (Optional) Cipher output after removing preamble", help="Leave empty to auto-derive")
    final_out = st.text_input("🏁 **Final output file (plaintext):**", help=r"e.g. C:\Users\You\Desktop\decoded.bin")
    sps = st.number_input("**Samples per symbol (SPS):**", min_value=1, value=2, key="rx_sps")
    mult = st.number_input("**Multiply constant:**", value=0.707, format="%.3f", key="rx_mult")

    if st.button("📥 **Start Receiving**"):
        try:
            if not rx_tmp or not final_out:
                st.error("Please provide RX TMP and Final output paths.")
                return

            # 1) Receive
            if mode == "Simulated (No-RF)":
                out = simulate_crc_receive(rx_tmp, sps, mult)
                st.success(f"Received TMP at {rx_tmp}")
                st.code(out)
            else:
                out = run_hw_rx(rx_tmp, sps, mult)
                st.success(f"Hardware RX wrote TMP at {rx_tmp}")
                st.code(out)

            # 2) Remove preamble (+CRC check in Sim) -> cipher_or_plain
            cipher_or_plain = cip_out.strip() or str(_default_with_suffix(rx_tmp, ".nopreamble"))
            if mode == "Simulated (No-RF)":
                out = simulate_remove_preamble_and_check_crc(rx_tmp, cipher_or_plain)
            else:
                out = run_remove_preamble(rx_tmp, cipher_or_plain)
            st.success("Preamble removed.")
            st.code(out)

            # 3) Decrypt if enabled, else just copy/rename result
            if use_aes:
                if not key_path:
                    st.error("AES is enabled — please provide the same Key file path used at TX in the sidebar.")
                    return
                out = aes_decrypt(cipher_or_plain, final_out, key_path)
                st.success("AES decryption complete.")
                st.code(out)
            else:
                # No AES: the content after preamble removal is already plaintext
                # Copy file (avoid overwrite issues by reading/writing)
                data = _p(cipher_or_plain).read_bytes()
                _p(final_out).parent.mkdir(parents=True, exist_ok=True)
                _p(final_out).write_bytes(data)
                st.success("Saved plaintext (no AES).")
                st.code(f"Copied {cipher_or_plain} → {final_out} ({len(data)} bytes)")

        except Exception as e:
            st.error(f"⚠️ RX failed: {e}")

    st.markdown("<p style='color:gray; font-size:12px;'>Use the same key file that was saved during encryption.</p>", unsafe_allow_html=True)

# -----------------------------
# Hardware wrappers (unchanged scripts)
# -----------------------------
def run_add_preamble(in_path: str, out_path: str) -> str:
    cmd = ["python", "addPreamble.py", "--input_path_tx", str(_p(in_path)), "--output_path_tx", str(_p(out_path))]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"addPreamble.py failed:\n{res.stderr}")
    return res.stdout or "(addPreamble.py OK)"

def run_hw_tx(tmp_path: str, sps: int, mult: float) -> str:
    cmd = ["python", "crctransmitter.py", "--filename-variable", str(_p(tmp_path)), "--spss", str(sps), "--multiplyconn", str(mult)]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"crctransmitter.py failed:\n{res.stderr}")
    return res.stdout or "(crctransmitter.py OK)"

def run_hw_rx(rx_tmp: str, sps: int, mult: float) -> str:
    cmd = ["python", "crcreceiver.py", "--recfilename-variable", str(_p(rx_tmp)), "--spss", str(sps), "--multiplyconn", str(mult)]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"crcreceiver.py failed:\n{res.stderr}")
    return res.stdout or "(crcreceiver.py OK)"

def run_remove_preamble(in_path: str, out_path: str) -> str:
    cmd = ["python", "removePreamble.py", "--input_path_rx", str(_p(in_path)), "--output_path", str(_p(out_path))]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"removePreamble.py failed:\n{res.stderr}")
    return res.stdout or "(removePreamble.py OK)"

# -----------------------------
# Main
# -----------------------------
def main():
    st.sidebar.title("QPSK Transceiver")
    mode = st.sidebar.selectbox("Backend", ["Simulated (No-RF)", "Hardware (BladeRF scripts)"])

    st.sidebar.markdown("### 🔒 AES (CBC) encryption")
    use_aes = st.sidebar.checkbox("Enable AES (CBC) encryption/decryption")
    key_path = st.sidebar.text_input("Key file path (required if AES on)", help="Same file for TX (save) and RX (load)")

    page = st.sidebar.radio("Choose:", ["🡵 Transmitter", "🡷 Receiver"])
    if page == "🡵 Transmitter":
        transmitter_page(mode, use_aes, key_path)
    else:
        receiver_page(mode, use_aes, key_path)

if __name__ == "__main__":
    main()
