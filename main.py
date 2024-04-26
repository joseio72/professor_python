# Professor Python


# Todos
# First , Put the flash cards into a  strage file like json.FileExistsError
# Then begin the termial program that will help you  study your flash cards.
# # edit exsitiing cards an add new ones
# maybe break up cards by lessons or topic.


import json


def main(obj):
    with open(file='./flashCards.json', mode='w') as file:
        json.dump(obj=obj, fp=file, indent=4)
    return


if __name__ == "__main__":
    main()
