import os

# Add preamble to file content
def add_preamble(input_path, output_path):
    """Adds a preamble and detection sequence to the file content and saves to a new file."""
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        exit(1)

    # Define preamble and detection sequences
    preamble = bytes([0b10101010]) * 3000  # Preamble sequence
    detect_sequence = bytes([0b00110011]) * 16  # Detection sequence (16 bytes long)
    
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
    # File path to add preamble
    #input_path = r"E:/Sem3-ENTC/CDP/30th dec/Files/Image/tx.jpg"
    input_path_tx = r"C:\Users\thili\OneDrive\Desktop\CDP\sample-min.png"

    #output_path = r"E:/Sem3-ENTC/CDP/30th dec/Files/Image/tx.tmp"
    output_path_tx = r"C:\Users\thili\OneDrive\Desktop\CDP\sample-min.tmp"

    # Add the preamble and save the output
    print("Adding preamble and saving the output...")
    add_preamble(input_path_tx, output_path_tx)
    print("Process completed successfully.")
