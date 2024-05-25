# Professor Python
# The purpose of this program is to test the retention of information.
# Take a test on all material
# Track Scores on material

import sys
import json
from os.path import isfile
from re import sub
import random
from rich.pretty import pprint
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime
from rich.prompt import Prompt
from rich import print
from rich.layout import Layout
from datetime import datetime, timezone
from rich.text import Text
import shutil
from rich import box
from rich.traceback import install
from rich.panel import Panel
import time

install(show_locals=True)
GLOSSARY_FILENAME = "./glossary.json"
SCORECARD_FILENAME = "./highScore.json"


def question(
    used_keys,
    content: dict = None,
    multiple_choice_number: int = 4,
):
    """
    Function is in charge of making a question.
    given the content and a number.
    """

    question = {
        "stem": "",
        "key": "",
        "alternatives": [],
    }

    rand_index = random.randint(0, len(content) - 1)
    # Here I want to make sure the question is not asked twice in a sinlge test.
    while rand_index in used_keys:
        rand_index = random.randint(0, len(content) - 1)
    used_keys.append(rand_index)

    set_up = random.choice([True, False])

    question["stem"] = content[rand_index][set_up]
    question["key"] = content[rand_index][not set_up]

    i = 1
    print(f"content {len(content)}")
    used_alternate_indexs = []
    while i < multiple_choice_number:
        alternatives_index = random.randint(0, len(content) - 1)
        if (
            alternatives_index == rand_index
            or alternatives_index in used_alternate_indexs
        ):
            continue
        question["alternatives"].append(content[alternatives_index][not set_up])
        used_alternate_indexs.append(alternatives_index)
        i += 1
    return question


def main():
    console = Console()
    console.clear()  # Just to start the program with a fresh console

    score = 0
    answered_questions = []
    with open(GLOSSARY_FILENAME, "r+b") as jsonFile:
        glossary_items = json.load(jsonFile)

    glossary_items = glossary_items.items()
    metadata = dict(list(glossary_items)[:4])
    data = list(glossary_items)[4:]

    for _ in range(len(data)):
        console.clear()  # Just to start the program with a fresh console
        item = question(used_keys=answered_questions, content=data)
        header_title = Text(metadata["certification"], justify="center")
        header_title.stylize("bold", 0, 6)
        header_subtitle = Text(metadata["topic"], justify="center")
        header_subtitle.stylize("bold", 0, 6)

        print("\n")
        print(
            Panel(
                header_title,
                title=f"{metadata['exam code']}",
                subtitle=header_subtitle,
            )
        )
        print("\n")
        stem = Text(item["stem"], justify="center")
        print(Panel(stem, title="Question"))
        print("\n")

        correct_index = random.randint(0, len(item["alternatives"]))

        item["alternatives"].insert(correct_index, item["key"])

        multiple_choices = list(zip(["a", "b", "c", "d"], item["alternatives"]))

        for choice in range(len(multiple_choices)):
            multiple_choice_option = Text(multiple_choices[choice][1], justify="center")
            print("\n")
            print(Panel(multiple_choice_option, title=multiple_choices[choice][0]))

        prompt_answer = Prompt.ask("ans?", choices=["a", "b", "c", "d", "exit"])
        if prompt_answer == "exit":
            # save and close.
            sys.exit()

        # Now we check for a match. if good add to he score else no points.
        for i, choice in enumerate(multiple_choices):
            if prompt_answer != choice[0] or i != correct_index:
                # we are looking for the choice that is what the user input.
                continue
            else:
                score += 1
                break

    # We print and save the score!!!!
    current_utc_time = datetime.now()
    formatted_utc_time = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")

    with open(SCORECARD_FILENAME, "r+b") as jsonFile:
        file_context = json.load(jsonFile)
    score_items = list(file_context.items())
    score_items.append((formatted_utc_time, score))
    with open(SCORECARD_FILENAME, "w") as jsonFile:
        json.dump(dict(score_items), jsonFile)

    console.clear()
    print("\n")
    print("\n")
    print("\n")
    score = sorted(score_items, key=lambda srce: srce[1], reverse=True)

    table = Table(title="HighScores!")
    table.add_column("Date", justify="left", style="cyan", no_wrap=True)
    table.add_column("Score", justify="center", style="magenta")

    # TOP 20 scores
    for index, eachScore in enumerate(score):
        table.add_row(str(eachScore[0]), str(eachScore[1]))
        if index == 19:
            break
    console.print(table)


if __name__ == "__main__":
    main()
