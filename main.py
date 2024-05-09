# Professor Python
# The purpose of this program is to test the retention of information.
# Take a test on Indivdual Lessons
# Take a test on all matiral
# add new matiral
# edit or remove old matiral

import json
import typer
from typing_extensions import Annotated
import os
import random
from rich.pretty import pprint
from rich import print
from datetime import datetime
import shutil
from typing import Optional
from rich.columns import Columns

app = typer.Typer(no_args_is_help=True)

MATERIAL = 'material.json'
GLOSSARY = 'glossary.json'
EXAM = 'CS0-003'
CWD = os.getcwd()
BACKUP_DESTINATION = '.bak'
PWD_FILES = os.listdir(path='.')


@app.command()
def backup( file: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """
    Command to backup the core matiral.
    Name of the file will be matiral<UTC>.json
    """
    if not file: return
    # Just check if the file is in the Dir
    if not os.path.isfile(file):
        print("File not found.")
        return
    try:
        file_name = os.path.splitext(file)
        # First move the cureent backup to the bak folder.
        # Iterate through the files of the dir
        utc_timestamp = str(datetime.utcnow().timestamp())
        backup_file_name = file_name[0] + '_' + utc_timestamp + file_name[1]
        backup_file_path = os.path.join(BACKUP_DESTINATION, backup_file_name)
        print("Backup File:", backup_file_path)
        # Last Create the new backup file.
        shutil.copyfile(file, backup_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
    return

@app.command()
def Challenge(
        test_length: Annotated[Optional[int], typer.Argument()] = 10,
        multiple_choice_number : Annotated[Optional[int], typer.Argument()] = 5
        ):
    """
    argument determinds the length of the  test.
    test is comprised of learning material with Question and answer.

    """
    # first we back up the File
    backup(GLOSSARY)
    # Goal is tp print one question at a time
    # have a user give an answer sheet.
    terms= None
    with open(GLOSSARY, 'r+b') as jsonFile:
        terms = json.load(jsonFile)

    term_keys = list(terms.keys())
    term_values = list(terms.values())
    score = None
    correct_key = random.choice(term_keys)  # Randomly choose a key from the dictionary
    
    correct_value = terms[question_key]  # Retrieve the value corresponding to the chosen key
    #random_values_list = random.sample(term_values, k = multiple_choice_number - 1)
    print(correct_key)
    print(correct_value)
    print(random_values_list)
    return

if __name__ == "__main__":
    app()
