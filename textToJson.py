# This is the driver program that extracts the artefact data from the 
# Artefact_Docs text files

# To run the program ensure the Artefact_Docs folder includes the relevant
# text files produced by the PDF to txt file extraction script

import json
import os
import text_parser

def main():
    # Specify the directory containing the .txt files
    folder_path = "Artefact_Docs"

    # Initialize an empty dictionary to store data from all files
    all_data = {}

    # Iterate through each .txt file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                text = file.read()
                chapters = text_parser.parse_text(text)
                # Store the data in the dictionary
                all_data[filename] = chapters

    with open("vase_details.json", "w") as json_file:
        json.dump(all_data, json_file, indent=4)
        # file.write(json_data)

if __name__ == "__main__":
    main()
