import os

# Function to remove both front and back preambles and detection sequences from a file
def remove_preamble(file_path, output_path):
    """Removes preambles and detection sequences from the input file and writes the cleaned content to a new file."""
    # Define the detection sequence and preamble
    detect_sequence = bytes([0b00110011]) * 16  # Detection sequence (16 bytes long)
    preamble = bytes([0b10101010]) * 3000       # Preamble sequence

    # Check if the input file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        exit(1)

    # Read the input file content
    with open(file_path, 'rb') as file:
        content = file.read()

    # Remove the front detection sequence and preamble
    start_index = content.find(detect_sequence)
    if start_index != -1:
        content = content[start_index + len(detect_sequence):]

    # Remove the back detection sequence and preamble
    end_index = content.rfind(detect_sequence)
    if end_index != -1:
        content = content[:end_index]

    # Write the cleaned content to the output file
    with open(output_path, 'wb') as output_file:
        output_file.write(content)
    
    print(f"Preambles removed and cleaned content saved to: {output_path}")

# Main script
if __name__ == "__main__":
    # Input file with preamble
    #input_path = r"E:/Sem3-ENTC/CDP/20th dec/Files/Audio/rx_preamble.tmp"
    input_path_rx = r"E:\Sem3-ENTC\CDP\30th Dec\Image\rx.tmp"
    
    # Output file path for the cleaned content
    #output_path = r"E:/Sem3-ENTC/CDP/20th dec/Files/Audio/cleaned_audio.wav"
    output_path = r"E:/Sem3-ENTC/CDP/30th dec/Image/rx.jpg"
    
    # Remove preamble and save cleaned content
    print("Removing preamble from the file...")
    remove_preamble(input_path_rx, output_path)
    print("Process completed successfully.")
