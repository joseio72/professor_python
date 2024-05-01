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
from rich.pretty import pprint
from rich import print
from datetime import datetime
import shutil
from typing import Optional
from rich.columns import Columns

app = typer.Typer(no_args_is_help=True)

MATERIAL_FILE_NAME = 'material'
NAME_OF_MATERIAL = 'CS0-003'
cwd = os.getcwd()
BACKUP_DESTINATION = '.bak'
PWD_FILES = os.listdir(path='.')


def move_old_backup():
    # Create the destination directory if it doesn't exist
    if not os.path.exists(BACKUP_DESTINATION):
        os.makedirs(BACKUP_DESTINATION)
    # Iterate through the files of the dir
    for file in PWD_FILES:
        # Check if the file starts with 'file_'
        if file.startswith(MATERIAL_FILE_NAME + '_'):
            # Construct the full path of the destination file
            destination_file = os.path.join(BACKUP_DESTINATION, file)
            # Move the file to the destination directory
            shutil.move(file, destination_file)
            print(f"Moved {file} to {BACKUP_DESTINATION}")


def backup_json_file(extension: str) -> None:
    try:
        # Just check if the file is in the Dir
        if not os.path.isfile(MATERIAL_FILE_NAME + extension):
            print("File not found.")
            return

        # First move the cureent backup to the bak folder.
        move_old_backup()

        # Last Create the new backup file.
        utc_timestamp = str(datetime.utcnow().timestamp())
        backup_file = MATERIAL_FILE_NAME + '_' + utc_timestamp + extension
        shutil.copyfile(MATERIAL_FILE_NAME + extension, backup_file)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.command()
def choose_lesson():
    # Want enter a lesson and work from there let use EXplore this idea.
    with open(MATERIAL_FILE_NAME, 'r+b') as file:
        jsn = json.load(file)
        pprint(jsn, expand_all=True)
        file.close()
    return


@app.command()
def login(
        name: str,
        email: Annotated[str, typer.Option(prompt=True)],
        ):
    """
    Soon Login information for users to learn about Indivdual topics
    """
    print(f"Hello {name}, your email is {email}")
    return


@app.command()
def backup(
        backup_extension:
        Annotated[Optional[str], typer.Argument()] = '.json') -> None:
    """
    Command to backup the core matiral.
    Name of the file will be matiral<UTC>.json
    """
    backup_json_file(extension=backup_extension)
    return


@app.command()
def Challenge(
        test_length: Annotated[Optional[int], typer.Argument()] = 10
        ):
    """
    argument determinds the length of the  test.
    test is comprised of learning material with Question and answer.
    """

    
    return


@app.command()
def create_Lesson(lesson_name: str):
    """
    arg name of new section or chapter. Command with format the name to \
    lower the text capitalization.
    add new section to the core material by adding the header of a new lesson.
    """
    backup_json_file()
    # Prep the name of the new lesson.name
    lesson_name.lower()
    # First gather the materials
    material = None
    with open(MATERIAL_FILE_NAME, 'r+b') as jsonFile:
        # TO DO
        # Some day we want to pull the most recent .bak in case of failure.
        material = json.load(jsonFile)

    # Next add in the name of the new lesson
    material[NAME_OF_MATERIAL][lesson_name] = {}
    print(material)
    # Last Write the new file.
    with open(MATERIAL_FILE_NAME, 'w') as jsonFile:
        json.dump(obj=material, fp=jsonFile, indent=4)
    return


if __name__ == "__main__":
    print(PWD_FILES)
    print(dir)
    app()
