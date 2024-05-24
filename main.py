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
from datetime import datetime
from rich.prompt import Prompt
from rich import print
from rich.layout import Layout
from rich.text import Text
import shutil
from rich import box
from rich.traceback import install
from rich.panel import Panel
import time

install(show_locals=True)


def randomTopicObject(bookTopic):
    topic = None
    with open(bookTopic, "r+b") as jsonFile:
        topic = json.load(jsonFile)
    return topic


def question(
    used_keys,
    topic: dict = None,
    multiple_choice_number: int = 4,
):
    """
    Function is in charge of making a question.
    given the content and a number.
    """

    if not topic:
        return

    topic_items = topic.items()

    content = list(topic_items)[4:]

    question = {
        "stem": "",
        "key": "",
        "alternatives": [],
    }

    rand_index = random.randint(0, len(content))
    # Here I want to make sure the question is not asked twice in a sinlge test.
    while rand_index in used_keys:
        rand_index = random.randint(0, len(content))
    used_keys.append(rand_index)

    set_up = random.choice([True, False])

    question["stem"] = content[rand_index][set_up]
    question["key"] = content[rand_index][not set_up]

    i = 1
    used_alternate_indexs = []
    while i < multiple_choice_number:
        alternatives_index = random.randint(0, len(content))
        if (
            alternatives_index == rand_index
            or alternatives_index in used_alternate_indexs
        ):
            continue
        question["alternatives"].append(content[alternatives_index][not set_up])
        used_alternate_indexs.append(alternatives_index)
        i += 1
    return question, dict(list(topic_items)[:4])


if __name__ == "__main__":
    console = Console()
    console.clear()  # Just to start the program with a fresh console
    answered_questions = []
    score_track = {"wrong": [], "right": [], "score": 0}
    test_length = 10
    topic = randomTopicObject("./glossary.json")

    for _ in range(test_length):
        console.clear()

        item, metadata = question(used_keys=answered_questions, topic=topic)

        header_title = Text(metadata["lesson"], justify="center")
        header_title.stylize("bold", 0, 6)
        header_subtitle = Text(metadata["topic"], justify="center")
        header_subtitle.stylize("bold", 0, 6)

        print("\n")
        print(
            Panel(
                header_title,
                title=f"{metadata['certification']} - {metadata['exam code']}",
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
            if prompt_answer != choice[0]:
                # we are looking for the choice that is what the user input.
                continue
            if i != correct_index:
                score_track["wrong"].append((item["stem"]))
            else:
                # Then Checking truth
                score_track["right"].append((item["key"]))
                score_track["score"] += 1
                break

    console.clear()
    # We print and save the score!!!!
    final_score = Text(str(score_track["score"]), justify="center")

    print("\n")
    print("\n")
    print("\n")
    print(
        Panel(
            final_score,
            title="!Score!",
        )
    )
    print("\n")
    for item in score_track["wrong"]:
        item_number = Text(item, justify="center")
        print("\n")
        print(Panel(item_number, title="wrong"))
    for item in score_track["right"]:
        item_number = Text(item, justify="center")
        print("\n")
        print(Panel(item_number, title="right"))
