import re
import os

# HEADER #
# For this file to work, you need to ensure that the file is in the same folder, or you edit the filename to include the path
# The major chapter number is the chapter as listed in the book,
# the sub chapter is as listed, they are seperated in the book as well.

# below is the main variables for this code. including the Regex expression, the user inputs, and the establishment of the dictionary
rx = re.compile(r'^\d+\b|^\*\d+\b|^\d+.\b|^\*\d+.\b')
filename = 'APPENDIX III -THE CAIVANO PAINTER.txt'
bruh = {}
key = ""
Chapter = input(' what the Major chapter number ')
sub_chapter = input(' what is the sub chapter name ')


# This fuction reads the file line by line and adds each block of text, seperated by white space
# to a new block in the blocks list
def read_blocks_from_file(filename):
    blocks = []
    with open(filename, 'r') as file:
        current_block = []
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # If the line is not empty
                current_block.append(line)
            else:  # If the line is empty, it marks the end of a block
                if current_block:  # If there are lines in the current block
                    blocks.append('\n'.join(current_block))
                    current_block = []  # Reset current_block for the next block
        # Append the last block if it's not empty
        if current_block:
            blocks.append('\n'.join(current_block))
    return blocks


#this function seperates the artifact and the ID which will be used as they key when stored in the dict
def filter_blocks(block, artifact):
    block = str(block)
    index = block.find("*")
    if block[0].isdigit() or block.startswith("*"):
        return block, artifact
    else:
        if index != -1:
            artifact = block[:index]
            block = block[index:]
            print(artifact)
            print(block)
            return block, artifact
        else:
            pattern = r"\d+"
            matches = re.finditer(pattern, block)
            indices = [match.start() for match in matches]
            for i in range(len(indices)):
                if indices[i] > 0 and not block[indices[i] + 1] == ")":
                    index = indices[i]
                    artifact = block[:index]
                    block = block[index:]
                    print(artifact)
                    print(block)
                    return block, artifact


#this sets blocks as the outcome of the read from blocks function
blocks = read_blocks_from_file(filename)

for i, line in enumerate(blocks):
    block, artifact_type = filter_blocks(blocks[i], key)
    blocks[i] = block
    key = artifact_type
    if key in bruh:
        m = rx.findall(block)
        j = str(m)
        h = j.lstrip("['")
        h = h[:-2]
        Image_ID = f"PP-{Chapter}-{h} - {sub_chapter}"
        bruh[key].append(Image_ID + ' ' + block)
    else:
        m = rx.findall(block)
        j = str(m)
        h = j.lstrip("['")
        h = h[:-2]
        Image_ID = f"PP-{Chapter}-{h} - {sub_chapter}"
        bruh[key] = [Image_ID + ' ' + block]
    print(bruh[key])
    print("Count: ", len(bruh[key]))
    print(blocks[i])



with open('./OUTPUT/' + filename + '-OUTPUT' + '.txt', "w") as file:
    for key in bruh:
        file.write(key + "\n")
        for value in bruh[key]:
           file.write(value + "\n\n")

