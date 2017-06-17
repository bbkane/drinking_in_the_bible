import collections
import json
import os
import sys


def clear_screen():
    # https://stackoverflow.com/a/4810595
    if sys.platform == 'darwin':
        os.system('clear')
    elif sys.platform == 'windows':  # TODO: text
        os.system('cls')


CHOICES = collections.OrderedDict([
    ('a', 'n/a'),
    ('s', 'negative'),
    ('d', 'conditionally negative'),
    ('f', 'neutral but something bad happened'),
    ('j', 'neutral'),
    ('k', 'neutral but something good happened'),
    ('l', 'conditionally positive'),
    (';', 'positive'),
    ('q', 'quit'),
])


def get_choice():
    for key, value in CHOICES.items():
        print(key, '::', value)
    choice = input('> ')
    while choice not in CHOICES:
        print('Invalid Choice!')
        choice = input('> ')
    return choice


def main():

    file_name = 'verse_runs_rated.json'
    with open(file_name, 'r') as verse_runs_file:
        verse_runs = json.load(verse_runs_file)

    total_runs = len(verse_runs)
    for index, verse_run in enumerate(verse_runs):
        if 'rating' not in verse_run:
            clear_screen()
            run_header = 'run {} of {}'.format(index + 1, total_runs)
            header = '{book_start} {chapter_start}:{verse_start} to {book_end} {chapter_end}:{verse_end}'.format(**verse_run)
            print(run_header, '\n\n', header, '\n\n', verse_run['verses'])
            choice = get_choice()
            if choice == 'q':
                break
            else:
                comment = input("Enter comment :: ")
                verse_run['rating'] = CHOICES[choice]
                verse_run['comment'] = comment

    with open('verse_runs_rated.json', 'w') as ratings_file:
        json.dump(verse_runs, ratings_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
