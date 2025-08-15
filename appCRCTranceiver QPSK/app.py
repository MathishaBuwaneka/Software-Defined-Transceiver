import streamlit as st
import subprocess

# Transmitter Page
def transmitter_page():
    st.title("🚀 **Transmitter**")
    st.markdown("<hr style='border:1px solid #f63366;'>", unsafe_allow_html=True)

    # File location input
    file_location1 = st.text_input("📂 **Enter file location:**", help="ex:C:\\Users\\Thisuka Inol\\Desktop\\gui.tx")
    file_location2 = st.text_input("**Enter file location to save tmp file:**")

    # Additional inputs
    samples_per_symbol = st.number_input("**Samples per symbol:**", min_value=1, value=2)
    multiply_constant = st.number_input("**Multiply constant:**", value=0.707,format="%.3f")

    # Start transmitting button
    if st.button("🦜 **Start Transmitting**"):
        if file_location1:
            # Build the command to execute the Python script
            command1 = [
                    "python",
                    "addPreamble.py",
                    "--input_path_tx", file_location1,
                    "--output_path_tx", file_location2
                    ]

            try:
                # Execute the external script
                result1 = subprocess.run(command1, text=True, capture_output=True)
                if result1.returncode == 0:
                    st.success(f"Tmp file saved to **{file_location2}**!")
                    st.text(f"Output:\n{result1.stdout}")
                    command2 = [
                            "python",
                            "crctransmitter.py",
                            "--filename-variable", file_location2,
                            "--spss", str(samples_per_symbol),
                            "--multiplyconn", str(multiply_constant)
                            ]

                    result2 = subprocess.run(command2, text=True, capture_output=True)
                    if result2.returncode == 0:
                        st.success("Transmission successfully!")
                        st.text(f"Output:\n{result2.stdout}")
                    else:
                        st.error("⚠️ Error occurred while executing the transmission script.")
                        st.text(f"Error Output:\n{result2.stderr}")
                else:
                    st.error("⚠️ Error occurred while adding to preamble.")
                    st.text(f"Error Output:\n{result1.stderr}")     
            except Exception as e:
                st.error(f"⚠️ Failed to execute the script: {e}")
        else:
            st.error("⚠️ Please enter a valid file location.")

    # Footer note
    st.markdown("<p style='color:gray; font-size:12px;'>Ensure the BladeRF device is properly connected before starting transmission.</p>", unsafe_allow_html=True)

# Receiver Page
def receiver_page():
    st.title("📡 **Receiver**")
    st.markdown("<hr style='border:1px solid #2c75c1;'>", unsafe_allow_html=True)

    # File destination address input
    file_destination2 = st.text_input("🏠 **Enter file destination address to:**")
    file_destination1 = st.text_input("**Enter file destination address to save tmp:**", help="ex:C:\\Users\\Thisuka Inol\\Desktop\\gui.txt")

    # Additional inputs
    samples_per_symbol = st.number_input("**Samples per symbol:**", min_value=1, value=2)
    multiply_constant = st.number_input("**Multiply constant:**", value=0.707,format="%.3f")

    # Start receiving button
    if st.button("📥 **Start Receiving**"):
        if file_destination1:
            # Build the command to execute the Python script
            command1 = [
                    "python",
                    "crcreceiver.py",
                    "--recfilename-variable", file_destination1,
                    "--spss",str(samples_per_symbol),
                    "--multiplyconn",str(multiply_constant)
                    ]

            try:
                # Execute the external script
                result1 = subprocess.run(command1, text=True, capture_output=True)
                if result1.returncode == 0:
                    st.success(f"Saved received Tmp file to **{file_destination1}**!")
                    st.text(f"Output:\n{result1.stdout}")
                    command2 = [
                            "python",
                            "removePreamble.py",
                            "--input_path_rx", file_destination1,
                            "--output_path", file_destination2
                            ]

                    result2 = subprocess.run(command2, text=True, capture_output=True)
                    if result2.returncode == 0:
                        st.success("Removing preamble successful!")
                        st.text(f"Output:\n{result2.stdout}")
                    else:
                        st.error("⚠️ Error occurred while removing the preamble.")
                        st.text(f"Error Output:\n{result2.stderr}")
                else:
                    st.error("⚠️ Error occurred while receiving Tmp file.")
                    st.text(f"Error Output:\n{result1.stderr}")     
            except Exception as e:
                st.error(f"⚠️ Failed to execute the script: {e}")
        else:
            st.error("⚠️ Please enter a valid file location.")

    # Footer note
    st.markdown("<p style='color:gray; font-size:12px;'>Ensure the BladeRF device is properly connected before starting reception.</p>", unsafe_allow_html=True)

# Main Page
def main():
    st.sidebar.title("QPSK Transmitter")
    page = st.sidebar.radio("Choose:", ["🡵 Transmitter", "🡷 Receiver"])

    if page == "🡵 Transmitter":
        transmitter_page()
    elif page == "🡷 Receiver":
        receiver_page()

if __name__ == "__main__":
    main()
