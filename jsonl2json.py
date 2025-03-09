import json

def convert_jsonl_to_createml(input_file, output_file):
    # Initialize the data list
    data = []

    # Process each line in the JSONL file
    with open(input_file, 'r') as input_f:
        for line in input_f:
            # Parse the JSON object
            json_obj = json.loads(line)

            # Extract the relevant fields
            text = json_obj.get('text', '')
            labels = json_obj.get('label', [])

            # Split the text into tokens
            tokens = text.split()

            # Initialize the label list with 'NONE' for each token
            token_labels = ['NONE'] * len(tokens)

            # Adjust the label positions based on word boundaries
            for start, end, label in labels:
                # Find the corresponding token positions for the label
                token_start = None
                token_end = None
                for i, token in enumerate(tokens):
                    if token_start is None and text.find(token) >= start:
                        token_start = i
                    if token_end is None and text.find(token) + len(token) >= end:
                        token_end = i + 1
                        break

                # Assign the label to the corresponding token range
                if token_start is not None and token_end is not None:
                    entity_tag = label.upper()  # Convert the entity label to uppercase for tagging
                    token_labels[token_start:token_end] = [entity_tag] * (token_end - token_start)

            # Create a dictionary for the current data instance
            instance = {
                "tokens": tokens,
                "labels": token_labels
            }

            # Add the instance to the data list
            data.append(instance)

    # Save the data list as JSON
    with open(output_file, 'w') as output_f:
        json.dump(data, output_f, indent=2)

    print(f"Conversion completed. Converted data saved to {output_file}.")

# Example usage: Provide input and output file paths
input_file = input('Drag and drop your input file here:').strip()
output_file = input('Drag and drop your output file here:').strip()
convert_jsonl_to_createml(input_file, output_file)
