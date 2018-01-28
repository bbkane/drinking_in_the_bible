from pathlib import Path
import argparse
import collections
import json
import os
import sys


DESCRIPTION = """
Rate the verses in a JSON file
"""


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-if', '--input_file', nargs='?', type=Path,
                        default=Path("~/Dropbox/Data/drinking_bible/verse_runs_rated.json"),
                        help="Input JSON file")
    parser.add_argument('-of', '--output_file', nargs='?', type=Path,
                        default=Path("~/Dropbox/Data/drinking_bible/verse_runs_rated.json"),
                        help="Output JSON file")
    args = parser.parse_args()
    # expand args
    args.input_file = args.input_file.expanduser()
    args.output_file = args.output_file.expanduser()
    return args


def clear_screen():
    # https://stackoverflow.com/a/4810595
    if sys.platform == 'darwin' or sys.platform == 'linux':
        os.system('clear')
    elif sys.platform == 'win32':
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
    args = parse_args()

    with args.input_file.open('r') as verse_runs_file:
        verse_runs = json.load(verse_runs_file)

    total_verse_runs = verse_runs['total_verse_runs']
    total_verse_count = verse_runs['total_verse_count']

    total_verses_so_far = 0

    for index, verse_run in enumerate(verse_runs['verse_runs']):

        total_verses_so_far += verse_run['verse_count']

        if 'rating' not in verse_run:
            clear_screen()

            percentage = (index + 1) / total_verse_runs * 100
            runs_left = total_verse_runs - (index + 1)
            run_header = f'run {index + 1} of {total_verse_runs} - {percentage:0.2f}% - {runs_left} runs left'

            verse_total_percent = total_verses_so_far / total_verse_count * 100
            total_verses_left = total_verse_count - total_verses_so_far
            verse_total_header = f'verses {total_verses_so_far} of {total_verse_count} - {verse_total_percent:0.2f}% - {total_verses_left} verses left'

            book_end = verse_run['book_end']
            book_start = verse_run['book_start']
            chapter_end = verse_run['chapter_end']
            chapter_start = verse_run['chapter_start']
            verse_count = verse_run['verse_count']
            verse_end = verse_run['verse_end']
            verse_start = verse_run['verse_start']

            header = f'{book_start} {chapter_start}:{verse_start} to {book_end} {chapter_end}:{verse_end}'

            print(run_header, verse_total_header, header, verse_run['verses'], sep='\n\n')
            choice = get_choice()
            if choice == 'q':
                break
            else:
                comment = input("Enter comment :: ")
                verse_run['rating'] = CHOICES[choice]
                verse_run['comment'] = comment

    with args.output_file.open('w') as ratings_file:
        json.dump(verse_runs, ratings_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
