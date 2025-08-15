import os
import argparse

# Function to remove both front and back preambles and detection sequences from a file
def remove_preamble(file_path, output_path):
    """Removes preambles and detection sequences from the input file and writes the cleaned content to a new file."""
    # Define the detection sequence and preamble
    detect_sequence = bytes([0b00110011]) * 5  # Detection sequence (16 bytes long)
    preamble = bytes([0b10101010]) * 100000       # Preamble sequence

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
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Remove preambles and detection sequences from a file.")
    parser.add_argument("--input_path_rx", required=True, help="Path to the input file with preambles.")
    parser.add_argument("--output_path", required=True, help="Path to save the cleaned content.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Extract paths
    input_path_rx = args.input_path_rx
    output_path = args.output_path
    
    # Remove preamble and save cleaned content
    print("Removing preamble from the file...")
    remove_preamble(input_path_rx, output_path)
    print("Process completed successfully.")
