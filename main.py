# Professor Python
# The purpose of this program is to test the retention of information.
# Take a test on all material
# Track Scores on material

import json
from os.path import isfile
from re import sub
import os
import random
from rich.pretty import pprint
from rich import print
from datetime import datetime
import shutil
from rich.columns import Columns

CALL_RANDIT = lambda x: random.randint(0,len(x)-1)


def randomTopicObject(bookTopic):
    topic = None
    with open(bookTopic, 'r+b') as jsonFile:
        topic = json.load(jsonFile)
    return topic


def Challenge(
        topic: dict = None,
        multiple_choice_number : int = 4
        ):
    """
    argument determinds the length of the  test and the content we are testing on
    test is comprised of learning material with Question and answer.

    """
    if not topic: return

    admin_headers = {key: sub_topic[key] for key in list(topic.keys())[:6]}

    content = {key: sub_topic[key] for key in list(topic.keys())[6:]}

    topic_keys = list(content.keys())

    topic_values = list(content.values())

    item={
        'stem': '',
        'key':'',
        'alternatives':[],
    }

    #if random.choice([True,False]):
    used_indexs = []
    if True: 
        index = CALL_RANDIT(topic_keys)
        print(index)
        item['stem'] = topic_keys[index]  
        item['key'] = topic_values[index] 
        i = 0
        while i < multiple_choice_number:
            alt_index =  CALL_RANDIT(topic_values)
            if index == alt_index or alt_index in used_indexs: 
                print(used_indexs)
                continue
            item['alternatives'].append(topic_values[alt_index])
            used_indexs.append(alt_index)
            i+=1 
    return item , admin_headers

if __name__ == "__main__":

    score = 0 
    test_length = 10
    for _ in range(test_length):
        content = [i for i in os.listdir() if i.endswith('.json')]
        randomContentIndex = CALL_RANDIT(content)
        topic = randomTopicObject(content[randomContentIndex])
        item, metadata = Challenge(topic)
        print(metadata)
        print(item)
