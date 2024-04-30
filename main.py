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
from rich.columns import Columns


NAME_OF_MATERIAL = 'CS0-003'
MATERIALS = 'material.json'
app = typer.Typer(no_args_is_help=True)


def backup_json_file(backup_extension='.bak'):
    try:
        if not os.path.isfile(MATERIALS):
            print("File not found.")
            return
        utc_timestamp = str(datetime.utcnow().timestamp())
        backup_file = MATERIALS + utc_timestamp + backup_extension
        shutil.copyfile(MATERIALS, backup_file)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.command()
def materials_structure(name: str):
    """

    add  new section to the core material by adding the header of a new lesson.
    The meaning of lesson and chapter are the same here.
    """
    # First gather the materials
    return


@app.command()
def choose_lesson():
    with open(MATERIALS, 'r+b') as file:
        jsn = json.load(file)
        pprint(jsn, expand_all=True)
        file.close()
    return


@app.command()
def login(
        name: str,
        email: Annotated[str, typer.Option(prompt=True)],
        ):
    print(f"Hello {name}, your email is {email}")
    return


@app.command()
def backup_material() -> None:
    """
    Command to backup the core matiral.
    Name of the file will be matiral<UTC>.json.bak
    """
    backup_json_file()
    return


@app.command()
def show_lessons() -> None:
    """
    Display a colum of all curret lessons
    """
    material = None
    with open(MATERIALS, 'r+b') as jsonFile:
        material = json.load(jsonFile)
    lessons = material[NAME_OF_MATERIAL].keys()
    columns = Columns(lessons, equal=True, expand=True)
    print(columns)
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
    with open(MATERIALS, 'r+b') as jsonFile:
        # TO DO
        # Some day we want to pull the most recent .bak in case of failure.
        material = json.load(jsonFile)

    # Next add in the name of the new lesson
    material[NAME_OF_MATERIAL][lesson_name] = {}
    print(material)
    # Last Write the new file.
    with open(MATERIALS, 'w') as jsonFile:
        json.dump(obj=material, fp=jsonFile, indent=4)
    return


@app.command()
def create_topic(name: str):
    """
    add new section to the core material by adding the header of a new lesson.
    """
    # First gather the materials
    print(name)
    material = None
    with open(MATERIALS, 'r+b') as jsonFile:
        material = json.load(jsonFile)
    print(material)
    return


if __name__ == "__main__":
    files = os.getcwd()
    dir = os.listdir(path='.')
    print(files)
    print(dir)
    app()
