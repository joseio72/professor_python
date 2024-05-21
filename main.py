# Professor Python
# The purpose of this program is to test the retention of information.
# Take a test on all material
# Track Scores on material

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
    with open(bookTopic, 'r+b') as jsonFile:
        topic = json.load(jsonFile)
    return topic


def question(
        topic: dict = None,
        multiple_choice_number : int = 4
        ):
    """
    Function is in charge of making a question. 
    given the content and a number.
    """

    if not topic: return

    items = topic.items()

    content = list(items)[4:]

    question={
        'stem': '',
        'key':'',
        'alternatives':[],
    }

    #if random.choice([True,False]):
    if True: 
        index = random.randint(0,len(content))
        question['stem'] = content[index][0]
        question['key'] = content[index][1]

        i = 1
        used_indexs = []
        while i < multiple_choice_number:
            alternatives_index = random.randint(0,len(content))
            if index == alternatives_index or alternatives_index in used_indexs: 
                continue
            question['alternatives'].append(content[alternatives_index][1])
            used_indexs.append(alternatives_index)
            i+=1 

    return question , dict(list(items)[:4])


if __name__ == "__main__":
    console = Console()
    console.clear() # Just to start the program with a fresh console
    score = 0 
    test_length = 10
    topic = randomTopicObject('./glossary.json')

    for _ in range(test_length):
        item, metadata = question(topic)

        header_title = Text(metadata['lesson'], justify='center')
        header_title.stylize("bold", 0, 6)
        header_subtitle = Text(metadata['topic'], justify='center')
        header_subtitle.stylize("bold", 0, 6)

        print('\n')
        print(Panel(header_title,
                    title=f"{metadata['certification']} - {metadata['exam code']}",
                    subtitle=header_subtitle))
        print('\n')


        question = Text(item['stem'], justify='center')
        print(Panel(question,title="Question"))
        print('\n')

        index = random.randint(0, len(item['alternatives']))

        item['alternatives'].insert(index, item['key'])
        
        multiple_choices = list(zip(["A","B","C","D"],item['alternatives']))
        
        for choice in range(len(multiple_choices)):
            multiple_choice_option = Text(multiple_choices[choice][1], justify='center')
            print(Panel(multiple_choice_option,title=multiple_choices[choice][0]))




        choice = Prompt.ask("your ans? ", choices=["D","C", "B", "A"], default="None")
        print(choice)
        console.clear()



