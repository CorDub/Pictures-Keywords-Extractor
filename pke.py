import subprocess
import os
import re
from pathlib import Path

def extract_keywords(target_folder):
    exiftool_path = Path("Image-ExifTool-12.82", "exiftool")
    subprocess.run(['perl', f'{exiftool_path}', '-j', f'{target_folder}', '-Subject', '-w', '.txt'])

def create_kw_csv(target_folder):
### Encode the target folder:
    folder = os.fsencode(target_folder)

    ### Check if there's a keywords.csv file in there and delete it
    keywords_path = Path(f"{target_folder}", "keywords.csv")
    if os.path.exists(keywords_path):
        os.remove(keywords_path)
        print("deleted keywords.csv")

    ### Check if there's a could_not_be_parsed.csv file in there and delete it
    could_not_be_parsed_path = Path(f"{target_folder}", "could_not_be_parsed.csv")
    if os.path.exists(could_not_be_parsed_path):
        os.remove(could_not_be_parsed_path)
        print("deleted keywords.csv")

    ### Go through every file of the folder, but....
    for file in os.listdir(folder):
        filename = os.fsdecode(file)

        ###... only if it's a text file:
        if filename.endswith(".txt"):
            ### Get the content:
            filename_path = Path(f"{target_folder}", filename)
            opened = open(filename_path, "r")
            content = opened.read()

            ### Process image names first:
            # image_name = re.findall(r"[AL]+\d+[_Original]+[.][a-z]{3}", content)[0]
            # image_name = image_name.replace("_Original", "")
            image_name = filename[:-4]

            ### Then get to keywords:
            split_res = re.split('\"Subject\":', content)
            keywords = split_res[1]
            keywords = keywords[1:-4]
            keywords = keywords.replace(']', '')
            keywords = keywords.replace('[', '')
            keywords = keywords.replace('"', '')

            ### Write this into a csv
            with open(keywords_path, "a") as file:
                file.write(f"{image_name},{keywords}\n")
            opened.close()

def find_stragglers(target_folder):
    ### Encode the target folder:
    folder =  os.fsencode(target_folder)

    ### Prepare return variable:
    not_parsed = []

    ### Go through every file in the folder:
    for file in os.listdir(folder):
        filename = os.fsdecode(file)

        ### Check whether a txt file with the same name has been produced and store its name if no
        if not os.path.exists(f"{target_folder}/{filename[:-4]}.txt") and filename != "keywords.csv":
            not_parsed.append(filename)
            print(f"{filename} added to not_parsed")
            ### Write this into a separate csv
            with open(f"{target_folder}/could_not_be_parsed.csv", "a") as file:
                file.write(f"{filename}\n")

    return not_parsed

def clean_up(target_folder):
    ### Encode the target folder:
    folder =  os.fsencode(target_folder)

    ### Go through every file in the folder:
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if os.path.exists(f"{target_folder}/{filename[:-4]}.txt"):
            os.remove(f"{target_folder}/{filename[:-4]}.txt")
            print(f"deleted {filename[:-4]}.txt")

def extract_csv_kw(target_folder):
    extract_keywords(target_folder)
    create_kw_csv(target_folder)
    not_parsed = find_stragglers(target_folder)
    clean_up(target_folder)
    return not_parsed
