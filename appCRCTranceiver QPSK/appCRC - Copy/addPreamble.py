import os
import argparse

# Add preamble to file content
def add_preamble(input_path, output_path):
    """Adds a preamble and detection sequence to the file content and saves to a new file."""
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        exit(1)

    # Define preamble and detection sequences
    preamble = bytes([0b10101010]) * 200000  # Preamble sequence
    detect_sequence = bytes([0b00110011]) * 5  # Detection sequence (16 bytes long)
    
    # Read the original file content
    with open(input_path, 'rb') as input_file:
        original_content = input_file.read()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write preamble, detection sequence, original content, detection sequence, and preamble
    with open(output_path, 'wb') as output_file:
        output_file.write(preamble + detect_sequence + original_content + detect_sequence + preamble)
    
    print(f"Preamble added and file saved to: {output_path}")

# Main script
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Add a preamble and detection sequence to a file.")
    parser.add_argument("--input_path_tx", required=True, help="Path to the input file.")
    parser.add_argument("--output_path_tx", required=True, help="Path to save the output file.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Extract paths
    input_path_tx = args.input_path_tx
    output_path_tx = args.output_path_tx
    
    # Add the preamble and save the output
    print("Adding preamble and saving the output...")
    add_preamble(input_path_tx, output_path_tx)
    print("Process completed successfully.")
