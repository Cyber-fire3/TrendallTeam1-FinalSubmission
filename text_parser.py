# The parse_text function requires a text file as an argument input
# Using various regex patterns it identifies artefact attributes
# returning an artefacts JSON file

# The returned JSON can then be used in the MongoDB database to
# provide formatted front-end artefact information

import re


def parse_text(text):
    # Split the text into lines
    lines = text.split("\n")

    # Initialise variables to store artefact data and temp values
    artefacts = []
    current_chapter = None
    current_artefact_type = None
    current_imageID = None
    current_painter = None
    current_artefact_number = None
    current_plate = None
    current_url = None
    current_provenance = None
    current_dimensions = None
    current_description = ""
    first_line = True

    # Define regular expression patterns for extracting specific artefact data
    artefact_number_pattern = r"PP-\d+-(\*?\d+)"
    chapter_pattern = r"(?<=2\.)(.*)"
    painter_pattern = r"- (.+?) (\d|\*)"
    # Provenance requires multiple conditions given the dynamic text environments
    provenance_pattern = r"\s+(?:\*\d+|\d+)\s+(.+?)\sHt\.?"
    provenance_pattern_condition1 = r"\s+(?:\*\d+|\d+)\s+(.+)"
    provenance_pattern_condition1_last = r"(?i)^(.*?)ht\."
    provenance_pattern_condition2 = r"\s+(?:\*\d+|\d+)\s+(.+?)\sDiam\.?"
    dimensions_pattern = r"Ht\.?.*?(?=\(i\)|\[b\)|PLATE|$)"
    publications_pattern = r"PLATE.*|P L A.*|PP,.*|^LCS.*"
    publications_pattern_stop = r"(.*?)(?=\[a\))|(.*?)(?=\(a\))"
    description_pattern = r"\[a\).*|\(a\).*"
    plate_pattern = r"PLATE \d+|P L A T E \d+|PLATE\d+"

    # Flags and temporary variables for concatenation of multi-line values
    above_line_blank = False
    provenance_concat_lines = ""
    publication_concat_lines = ""
    pub_pattern_found = False
    pub_stop_found = False
    description_concat_lines = ""
    desc_pattern_found = False
    plate_pattern_found = False

    # Iterate over each line in the text
    for line in lines:
        # Check if the line is blank
        if line.strip() == "":
            # Set flag to indicate the previous line was blank
            above_line_blank = True
            # Reset flags and concatenation variables for the next artefact block
            pub_pattern_found = False
            pub_stop_found = False
            publication_concat_lines = ""
            desc_pattern_found = False
            description_concat_lines = ""
            plate_pattern_found = False
            continue

        # Process the first line to extract chapter information
        if first_line:
            chapter_match = re.search(chapter_pattern, line)
            if chapter_match:
                current_chapter = chapter_match.group(0).strip()
            else:
                current_chapter = line.strip()
            first_line = False
            continue

        # Reset artefact type if a new artefact block is detected
        if not line.startswith("PP-") and above_line_blank:
            current_artefact_type = None

        # Set new artefact type if it's not already set
        if current_artefact_type is None:
            current_artefact_type = line.strip()
            above_line_blank = False
            continue

        # Process first line of an artefact block
        if line.startswith("PP-") and above_line_blank:
            # Reset all artefact-specific fields
            current_imageID = None
            current_painter = None
            current_artefact_number = None
            current_plate = None
            current_provenance = None
            current_dimensions = None
            current_publications = None
            current_description = ""

            # Extract artefact-specific information from the line

            # Extracts the image_ID
            current_imageID = line.split()[0]

            # Extracts artefact_number
            current_artefact_number_match = re.search(artefact_number_pattern, line)
            if current_artefact_number_match:
                current_artefact_number = current_artefact_number_match.group(1)

            # Extracts painter
            current_painter_match = re.search(painter_pattern, line)
            if current_painter_match:
                current_painter = current_painter_match.group(1)

            # Extracts provenance
            current_provenance_match = re.search(
                provenance_pattern, line, re.IGNORECASE
            )
            if current_provenance_match:
                current_provenance = current_provenance_match.group(1)
            # Provenance extraction is complex, requires multiple regex patterns to find
            elif current_provenance_match is None:
                current_provenance_match = re.search(
                    provenance_pattern_condition2, line, re.IGNORECASE
                )
                if current_provenance_match:
                    current_provenance = current_provenance_match.group(1)
                if current_provenance_match is None:
                    current_provenance_match = re.search(
                        provenance_pattern_condition1, line, re.IGNORECASE
                    )
                    if current_provenance_match:
                        result = current_provenance_match.group(1)
                        provenance_concat_lines = result + " "

            # Extract dimensions
            current_dimensions_match = re.search(
                dimensions_pattern, line, re.IGNORECASE
            )
            if current_dimensions_match:
                current_dimensions = current_dimensions_match.group(0).strip()

            # Extract publication
            current_publications_match = re.search(
                publications_pattern, line, re.IGNORECASE
            )
            if current_publications_match and not pub_pattern_found:
                publication_concat_lines = current_publications_match.group(0).strip()
                pub_pattern_found = True

            # Extract description
            current_description_match = re.search(
                description_pattern, line, re.IGNORECASE
            )
            if current_description_match:
                description_concat_lines = current_description_match.group(0).strip()

            # Extract plate
            current_plate_match = re.search(plate_pattern, line)
            if current_plate_match and not plate_pattern_found:
                current_plate = current_plate_match.group(0).strip()
                plate_pattern_found = True

            # Set to false to allow the next line to know its
            # position in an artefact block
            above_line_blank = False

        # Process subsequent artefact block line
        elif line.startswith("PP-") and not above_line_blank:
            # Reset all artefact-specific fields
            current_plate = None
            current_painter = None
            current_provenance = None
            current_dimensions = None
            current_publications = None
            current_description = ""

            # Extract artefact-specific information from the line

            # Extracts the image_ID
            current_imageID = line.split()[0]

            # Extracts artefact_number
            current_artefact_number_match = re.search(artefact_number_pattern, line)
            if current_artefact_number_match:
                current_artefact_number = current_artefact_number_match.group(1)

            # Extracts painter
            current_painter_match = re.search(painter_pattern, line)
            if current_painter_match:
                current_painter = current_painter_match.group(1)

            # Extracts provenance
            current_provenance_match = re.search(
                provenance_pattern, line, re.IGNORECASE
            )
            if current_provenance_match:
                current_provenance = current_provenance_match.group(1)
            # Provenance extraction is complex, requires multiple regex patterns to find
            elif current_provenance_match is None:
                current_provenance_match = re.search(
                    provenance_pattern_condition2, line, re.IGNORECASE
                )
                if current_provenance_match:
                    current_provenance = current_provenance_match.group(1)
                if current_provenance_match is None:
                    current_provenance_match = re.search(
                        provenance_pattern_condition1, line, re.IGNORECASE
                    )
                    if current_provenance_match:
                        result = current_provenance_match.group(1)
                        provenance_concat_lines = result + " "

            # Extract dimensions
            current_dimensions_match = re.search(
                dimensions_pattern, line, re.IGNORECASE
            )
            if current_dimensions_match:
                current_dimensions = current_dimensions_match.group(0).strip()

            # Extract publication
            current_publications_match = re.search(
                publications_pattern, line, re.IGNORECASE
            )
            if current_publications_match and not pub_pattern_found:
                publication_concat_lines = current_publications_match.group(0).strip()
                pub_pattern_found = True

            # Extract description
            current_description_match = re.search(
                description_pattern, line, re.IGNORECASE
            )
            if current_description_match:
                description_concat_lines = current_description_match.group(0).strip()

            # Extract plate
            current_plate_match = re.search(plate_pattern, line, re.IGNORECASE)
            if current_plate_match and not plate_pattern_found:
                current_plate = current_plate_match.group(0).strip()
                plate_pattern_found = True

        # Process non-empty lines that are not artefact headers
        elif line != "" and not above_line_blank:
            # Some imageID values will include *, this removes the character
            if current_imageID:
                current_imageID = current_imageID.replace("*", "")

            # Some artefact_number values will include *, this removes the character
            if current_artefact_number:
                current_artefact_number = current_artefact_number.replace("*", "")

            # Concatenate strings to the provenance value for an artefact
            # The provenance may exist on multiple lines of an artefact block
            current_provenance_match = re.search(
                provenance_pattern_condition1_last, line
            )
            if current_provenance_match:
                result = current_provenance_match.group(1)
                provenance_concat_lines += result
                current_provenance = provenance_concat_lines
            provenance_concat_lines += line + " "

            # Look for publications data in line
            current_publications_match = re.search(
                publications_pattern, line, re.IGNORECASE
            )
            # Searches for the end of publications data, recycles variable for
            # later lines to avoid overriding correct data
            current_publications_stop_match = re.search(
                publications_pattern_stop, line, re.IGNORECASE
            )

            # Extract publications

            # Finds a regex pattern match and that pub_pattern has not already
            # been found, nor has a stop been found
            if (
                current_publications_match
                and not pub_pattern_found
                and not pub_stop_found
            ):
                publication_concat_lines = current_publications_match.group(0).strip()
                pub_pattern_found = True
            # Finds a regex pattern match when pub_pattern has been found
            elif current_publications_match and pub_pattern_found:
                publication_concat_lines += (
                    " " + current_publications_match.group(0).strip()
                )
            # Finds a regex pattern stop match when pub_pattern has been found
            elif current_publications_stop_match and pub_pattern_found:
                publication_concat_lines += (
                    " " + current_publications_stop_match.group(0).strip()
                )
                pub_pattern_found = False
                pub_stop_found = True
            # A catch all which concatenates the whole line if a stop was not found
            # but a pattern was.
            elif pub_pattern_found:
                publication_concat_lines += " " + line
            current_publications = publication_concat_lines.strip()

            # Extract description

            current_description_match = re.search(
                description_pattern, line, re.IGNORECASE
            )
            # Extract beginning of description if match found
            if current_description_match:
                description_concat_lines += current_description_match.group(0).strip()
                desc_pattern_found = True
            # If match already found continue concatentating line to description until
            # the end of the artefact block
            elif desc_pattern_found:
                description_concat_lines += " " + line
            current_description = description_concat_lines.strip()

            # If current_plate exists replaces " " and "E" with appriate values
            if current_plate:
                current_plate = (
                    current_plate.replace(" ", "").replace("E", "E ").upper()
                )

            # Prepare artefact data
            artefact_data = {
                "ImageId": current_imageID,
                "Chapter": current_chapter,
                "Artefact Type": current_artefact_type,
                "Painter": current_painter,
                "Artefact Number": current_artefact_number,
                "Plate": current_plate,
                "PlateURL": current_url,
                "Provenance": current_provenance,
                "Physical Dimensions": current_dimensions,
                "Publications": current_publications,
                "Description": current_description,
            }

            # Update or add the artefact data to the list
            existing_index = None
            for index, artefact in enumerate(artefacts):
                if artefact["ImageId"] == current_imageID:
                    existing_index = index
                    break

            if existing_index is not None:
                artefacts[existing_index] = artefact_data
            else:
                artefacts.append(artefact_data)

            # Update the plate URL
            if current_plate is None:
                current_url = None
            else:
                modified_plate = current_plate.replace(" ", "+")
                URL = (
                    "https://artefactimages.s3.ap-southeast-2.amazonaws.com/"
                    + modified_plate
                    + ".jpeg"
                )
                current_url = URL

    return artefacts
