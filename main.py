# Professor Python
# The purpose of this program is to test the retention of information.
# Take a test on all material
# Track Scores on material

import json
from os.path import isfile
from re import sub
from typing_extensions import Annotated
import os
import random
from rich.pretty import pprint
from rich import print
from datetime import datetime
import shutil
from rich.columns import Columns
from typing import Optional

def Challenge(
        test_length: int  = 10,
        multiple_choice_number : int = 5
        ):
    """
    argument determinds the length of the  test.
    test is comprised of learning material with Question and answer.

    """
    print(f'Test Length ${test_length}')
    print(f'choice number ${multiple_choice_number}')
    content = [i for i in os.listdir() if i.endswith('.json')]

    #Right now th program does not care about memory saving
    score = None
    
    for _ in range(test_length):
        call_randit = lambda x: random.randint(0,len(x)-1)
        randomContentIndex = call_randit(content)

        selected_SubTopic = content[randomContentIndex]
        print(selected_SubTopic)

        sub_topic = None
        with open(selected_SubTopic, 'r+b') as jsonFile:
            sub_topic = json.load(jsonFile)

        #  In this protion of the code base we are just taking the admin information out of the varible and giving it a # %%
        #  Location  just to keep this apart in admin_headers. 
        admin_headers = {key: sub_topic[key] for key in list(sub_topic.keys())[:6]}

        # Then just removing them from the subtopic just to have some clean  Term and definitions.
        sub_topic = {key: sub_topic[key] for key in list(sub_topic.keys())[6:]}

        topic_keys = list(sub_topic.keys())
        topic_values = list(sub_topic.values())
        
        #Coin flip to determine the term or defintion.
        coin_flip = random.choice([True,False])
        
        question={
            'prompt': '',
            'choices':[],
        }

        if coin_flip: 
            # terms
            question['prompt'] = topic_keys[call_randit(topic_keys)]  # Randomly choose a key from the dictionary
            #Now we all the choices
            #First fill the bad choices
            question['choices'] = []
            random_index = random.randint(0, multiple_choice_number - 1)
            question['choices'].insert(random_index, 6)
        else: 
            #Definitions
            question['prompt'] = topic_values[call_randit(topic_values)]  # Randomly choose a key from the dictionary
            #Now we all the choices
            #First fill the bad choices
            question['choices'] = []
            random_index = random.randint(0, multiple_choice_number - 1)
            question['choices'].insert(random_index, 6)

        print(question)
        print('\n')
    return

if __name__ == "__main__":
    Challenge()
