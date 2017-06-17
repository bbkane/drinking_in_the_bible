import json
import os
import sys


def clear_screen():
    # https://stackoverflow.com/a/4810595
    if sys.platform == 'darwin':
        os.system('clear')
    elif sys.platform == 'windows':  # TODO: text
        os.system('cls')


def main():
    with open('verse_runs.json', 'r') as verse_runs_file:
        verse_runs = json.load(verse_runs_file)

    total_runs = len(verse_runs)
    for index, verse_run in enumerate(verse_runs):
        clear_screen()
        run_header = 'run {} of {}'.format(index + 1, total_runs)
        header = '{book_start} {chapter_start}:{verse_start} to {book_end} {chapter_end}:{verse_end}'.format(**verse_run)
        print(run_header, '\n\n', header, '\n\n', verse_run['verses'])
        choice = input('> ')
        if choice == 'q':
            break


if __name__ == "__main__":
    main()
