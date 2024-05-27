# Professor Python
# The purpose of this program is to test the retention of information.
# Take a test on all material
# Track Scores on material
#
#
import json
import random
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime
import os
from rich.prompt import Prompt
from rich.text import Text
from rich.traceback import install
from rich.panel import Panel

install(show_locals=True)
GLOSSARY_FILENAME = "glossary.json"
SCORECARD_FILENAME = "highScore.json"


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


def main(terms_file, score_file):
    console = Console()
    console.clear()  # Just to start the program with a fresh console

    score = 0
    answered_questions = []
    with open(terms_file, "r+b") as jsonFile:
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
        print("\n")
        print("\n")
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

        rich_confirm = False
        while not rich_confirm:
            prompt_answer = Prompt.ask("ans?", choices=["a", "b", "c", "d", "exit"])

            if prompt_answer == "exit":
                # save and close.
                rich_confirm = True
                console.clear()
                break

            rich_confirm = Prompt.ask(
                f"Type {prompt_answer} again to confirm you answer {prompt_answer}"
            )

            if prompt_answer != rich_confirm:
                rich_confirm = False
                continue

            # Now we check for a match. if good add to he score else no points.
            for i, choice in enumerate(multiple_choices):
                if prompt_answer != choice[0] or i != correct_index:
                    # we are looking for the choice that is what the user input.
                    continue
                else:
                    score += 1
                    break

        if (prompt_answer == "exit") and (rich_confirm is True):
            # save and close.
            console.clear()
            break

    console.clear()

    # Weprint and save the score!!!!
    current_utc_time = datetime.now()
    formatted_utc_time = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")

    with open(score_file, "r+b") as jsonFile:
        file_context = json.load(jsonFile)

    score_items = list(file_context.items())
    if score > 0:
        score_items.append((formatted_utc_time, score))
        with open(score_file, "w") as jsonFile:
            json.dump(dict(score_items), jsonFile)

    # console.clear()
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_in_dir = os.listdir(script_dir)
    if GLOSSARY_FILENAME in files_in_dir and SCORECARD_FILENAME in files_in_dir:
        score_file_path = os.path.join(script_dir, SCORECARD_FILENAME)
        terms_file_path = os.path.join(script_dir, GLOSSARY_FILENAME)

        main(terms_file=terms_file_path, score_file=score_file_path)
    else:
        print(
            f"'{GLOSSARY_FILENAME}' or '{SCORECARD_FILENAME}' not found in the directory."
        )
